from rest_framework import serializers
from Task.serializers import TaskSerializer
from User.serializers import UserSerializer
from .models import Board
from django.db.models import Q


class BoardSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tasks = TaskSerializer(many=True, read_only=True)
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ('id', 'author', 'title', 'tasks', 'users')
