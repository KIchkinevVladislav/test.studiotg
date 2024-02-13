from django.urls import path


app_name = 'games'

from .views import GameCreateView, TurnAPIView


urlpatterns = [
    path('new', GameCreateView.as_view(), name='new'),
    # path('turn', TurnAPIView.as_view(), name='turn'),
    # path('games/', GameListView.as_view(), name='games'),
]
