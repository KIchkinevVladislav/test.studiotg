from django.urls import path


app_name = 'games'

from .views import GameCreateView


urlpatterns = [
    path('new', GameCreateView.as_view(), name='new'),
    # path('games/', GameListView.as_view(), name='games'),
]