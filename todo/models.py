from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    memo = models.TextField(blank=True, verbose_name='Описание')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    datecompleted = models.DateTimeField(null=True, blank=True, verbose_name='Время выполнения')
    important = models.BooleanField(default=False, verbose_name='Важное')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.title


