from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404

from . forms import LoginForm, RegisterForm
from . import models
import json


def index(request, floor_id):
    """Обработчик главной страницы"""
    floor = models.Floor.objects.get(name=floor_id)
    data = {
        "floor": floor,
        "floors": models.Floor.objects.all(),
        "width": floor.image.width,
        "height": floor.image.height
    }
    return render(request, "floor.html", data)


def register_view(request):
    """Обработчик регистрации в системе"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            return redirect("/login") # Перенаправляем на вход
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form': form})
    
    
def login_view(request):
    """Обработчик страницы авторищзации в системе"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Используем встроенный login Django
            messages.success(request, f"Вы успешно вошли как {user.username}!")
            return redirect("/floor/1") # Перенаправляем на главную
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    """Обработчик для выхода из системы"""
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect('login') # Перенаправляем на страницу входа


def cabinet_view(request, cab):
    data = {
        'room': models.Room.objects.get(name=cab)
    }
    return render(request, "cabinet.html", data)

# TODO: Запретить не админам
def confirm_user(request, user_id):
    pass