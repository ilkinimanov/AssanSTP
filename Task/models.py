from django.db import models


class Subtask(models.Model):
    body            = models.TextField()
    is_completed    = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.body[:20]}...'


class Task(models.Model):
    title           = models.CharField(max_length=15)
    body            = models.TextField(blank=True)
    status          = models.CharField(max_length=15)
    subtasks        = models.ManyToManyField('Task.Subtask', related_name='subtask')
    deadline        = models.DateTimeField(blank=False, null=False)
    author          = models.ForeignKey('User.User', on_delete=models.CASCADE, related_name='author')
    users           = models.ManyToManyField('User.User', related_name='users')

    def __str__(self):
        return self.title
