from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from django.http import HttpResponse
from .math2speech import math2speech
from .PMRead import PM
from tutorvirtual.secret_key import MAIL,PWD


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
        try:
            response_data = pm.get_nota(int(response_data['text']))
            response_data['audio_url'] = 'media/voice.mp3'
            obj.generaAudio(response_data['nota']['contenido'],filename='./media/voice.mp3')
        except ValueError:      
            obj.generaAudio(response_data['text'],filename='./media/voice.mp3')
            response_data['audio_url'] = 'media/voice.mp3'
        response = Response(response_data, status=status.HTTP_200_OK)
        return response

