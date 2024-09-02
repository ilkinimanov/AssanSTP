from django.urls import include, path


urlpatterns = [
    path('api/task', include('Task.urls')),
    path('api/token', include('User.urls')),
    path('api/board', include('Board.urls')),
]
