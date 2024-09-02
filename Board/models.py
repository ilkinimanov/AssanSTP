from django.db import models


class Board(models.Model):
    title           = models.CharField(max_length=30)
    tasks           = models.ManyToManyField('Task.Task', related_name='tasks')

    def __str__(self):
        return self.title
