from django.db import models


class Board(models.Model):
    title           = models.CharField(max_length=30)
    tasks           = models.ManyToManyField('Task.Task', related_name='tasks')
    users           = models.ManyToManyField('User.User', related_name='users')
    author          = models.ForeignKey('User.User', related_name='author', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
