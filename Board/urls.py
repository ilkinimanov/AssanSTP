from django.urls import path
from .models import Board
from .views import BoardView

urlpatterns = [
    path('', BoardView),
    path('/<int:pk>', BoardView)
]
