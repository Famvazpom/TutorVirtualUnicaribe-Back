from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import re
from django.http import HttpResponse
from .math2speech import math2speech
from .PMRead import PM
from tutorvirtual.models import Contenido
from tutorvirtual.secret_key import MAIL,PWD
from django.utils.crypto import get_random_string
import pickle

with open('./tfidf.pkl','rb') as f: 
    chat = pickle.load(f)


with open('./normalizador.pkl','rb') as f: 
    normalizador = pickle.load(f)

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

    def get_response(self,input_statement):
        palabras = normalizador.normaliza_texto(input_statement).split(' ')
        existentes = [palabra for palabra in palabras if palabra in chat.columns]
        existentes = chat.loc[:,existentes]
        existentes.loc[:,'Total_sum']= existentes.sum(axis=1)
        existentes.loc[:,'Total_mean']= existentes.mean(axis=1)
        existentes=existentes.query('Total_mean == Total_mean.max()')
        return Contenido.objects.get(pk=existentes.index[0]+1)

    def post(self, request, *args, **kwargs):
        m2s = math2speech()
        response_data = {}
        input_statement = request.data.get('text')
        voicename = f'./media/{ get_random_string() }.mp3'
        obj = self.get_response(input_statement)
        response_data['text'] = obj.contenido
        response_data['autor'] = obj.autor
        response_data['titulo'] = obj.titulo
        response_data['audio_url'] = voicename
        result = re.split('\\\\begin{equation}\\n(.*)\\n\\\\end{equation}', obj.contenido)
        final = []

        for i in result:
            final += re.split('\$(.*)\$',i)
            
            
        for id,text in enumerate(final):
            if id > 0 and id%2==1:
                math = math2speech()
                c = math.procesaCadena(text,[char for char in text if char.isalpha()])
                final[id] = math.obtenCadena(0,c['arbol'])

        m2s.generaAudio(''.join(final),filename=voicename)

        response = Response(response_data, status=status.HTTP_200_OK)
        return response

        response_data = chatterbot.get_response(input_statement)
        response_data = response_data.serialize()
        voicename = f'./media/{ get_random_string() }.mp3'
        try:
            resulta = pm.get_nota(int(response_data['text']))['nota']
            response_data['text'] = resulta['contenido']
            response_data['autor'] = resulta['autor']['nombre']
            response_data['titulo'] = resulta['titulo']
            response_data['audio_url'] = voicename
            result = re.split('\\\\begin{equation}\\n(.*)\\n\\\\end{equation}', resulta['contenido'])
            final = []

            for i in result:
                final += re.split('\$(.*)\$',i)
                
                
            for id,text in enumerate(final):
                if id > 0 and id%2==1:
                    math = math2speech()
                    c = math.procesaCadena(text,[char for char in text if char.isalpha()])
                    final[id] = math.obtenCadena(0,c['arbol'])

            obj.generaAudio(''.join(final),filename=voicename)
        except ValueError:      
            obj.generaAudio(response_data['text'],filename=voicename)
            response_data['audio_url'] = voicename
        response = Response(response_data, status=status.HTTP_200_OK)
        return response

