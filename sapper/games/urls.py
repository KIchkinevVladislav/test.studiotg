from django.urls import path
from .views import GameCreateView, TurnAPIView

app_name = 'games'


urlpatterns = [
    path('new', GameCreateView.as_view(), name='new'),
    path('turn', TurnAPIView.as_view(), name='turn'),
]
