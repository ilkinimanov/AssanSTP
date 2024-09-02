from rest_framework import serializers
from User.serializers import UserSerializer
from .models import Task, Subtask


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ('id', 'body', 'is_completed')


class TaskSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, read_only=True)
    users = UserSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'body', 'status', 'subtasks', 'users', 'author')
