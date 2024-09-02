from django.urls import path
from .views import TaskView, SubtaskView

urlpatterns = [
    path('', TaskView),
    path('/<int:pk>', TaskView),
    path('/subtask', SubtaskView),
    path('/subtask/<int:pk>', SubtaskView)
]
