from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import re
from django.http import HttpResponse
from .math2speech import math2speech
from .PMRead import PM
from tutorvirtual.secret_key import MAIL,PWD
from django.utils.crypto import get_random_string

pm = PM(MAIL,PWD)
pm.conecta()

chatterbot = ChatBot(
    'MathIAs',
    io_adapter="chatterbot.adapters.io.JsonAdapter",
    database_uri='sqlite:///chatterbot.sqlite3',
    read_only=True
)

class ChatterBotView(views.APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        data = {
            'error': 'You should make a POST request to this endpoint.'
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        obj = math2speech()
        input_statement = request.data.get('text')

        response_data = chatterbot.get_response(input_statement)
        response_data = response_data.serialize()
        voicename = f'./media/{ get_random_string() }.mp3'
        try:
            response_data = pm.get_nota(int(response_data['text']))
            response_data['audio_url'] = voicename
            result = re.split('\\\\begin{equation}\\n(.*)\\n\\\\end{equation}', response_data["nota"]['contenido'])

            for id,text in enumerate(result):
                if id > 0 and id%2==1:
                    math = math2speech()
                    c = math.procesaCadena(text,[char for char in text if char.isalpha()])
                    result[id] = math.obtenCadena(0,c['arbol'])
            obj.generaAudio(''.join(result),filename=voicename)
        except ValueError:      
            obj.generaAudio(response_data['text'],filename=voicename)
            response_data['audio_url'] = voicename
        response = Response(response_data, status=status.HTTP_200_OK)
        return response

