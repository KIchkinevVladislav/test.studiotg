from django.shortcuts import render

from rest_framework.generics import CreateAPIView
from .serializers import GameSerializer
from .models import Game


class GameCreateView(CreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


# class GameListView(ListAPIView):
#     queryset = Game.objects.all()
#     serializer_class = GameSerializer