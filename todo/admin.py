from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    readonly_fields = ('created',) #отображение времени добавления в админке

admin.site.register(Todo, TodoAdmin)


