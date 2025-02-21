from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import TodoForm
from .models import Todo


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo\signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo\signupuser.html', {'form': UserCreationForm(), 'error':'Пользователь с таким именем уже существует'})
        else:
            return render(request, 'todo\signupuser.html', {'form': UserCreationForm(), 'error':'Пароли не совпадают'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo\loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request, 'todo\loginuser.html', {'form': AuthenticationForm(), 'error':'Имя пользователя и пароль не совпадают'})
        else:
            login(request, user)
            return redirect('currenttodos')


@login_required # доступ основным функциям только зарегистрированным пользователям
def logoutuser(request):
    if request.method == 'POST': # если logout будет инициировать GET запрос, браузер его выполнит в фоновом режиме и отменит вход пользователя
        logout(request)
        return redirect('home')


@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo\createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo\createtodo.html', {'form': TodoForm(),'error':'Переданы неверные данные'})


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True) # выводим задачи авторизованного пользователя также невыполненные задачи
    return render(request, 'todo/currenttodos.html', {'todos':todos})


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('datecompleted') # выполненные задачи,сортировка по дате
    return render(request, 'todo/completedtodos.html', {'todos':todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo) # instance=todo уточняем что изменяем уже существующий объект
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Неверная информация'})
   

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')