from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from django.http import HttpResponse
from .math2speech import math2speech

chatterbot = ChatBot(
    'Bot',
    io_adapter="chatterbot.adapters.io.JsonAdapter"
)
trainer = ListTrainer(chatterbot)

trainer.train([
    "Necesito ayuda en matematicas",
    "Que temas necesitas? puedo ayudarte en....",
    "Algebra",
    "Perfecto"]
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
        

        obj.generaAudio(response_data['text'],filename='./media/voice.mp3')
        response_data['audio_url'] = 'media/voice.mp3'
        response = Response(response_data, status=status.HTTP_200_OK)
        return response

