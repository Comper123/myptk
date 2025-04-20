from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect

from . forms import LoginForm


def index(request, floor_id):
    """Обработчик главной страницы"""
    data = {
        
    }
    return render(request, "floor.html", data)


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
            messages.error(request, "Ошибка входа. Пожалуйста, проверьте свои данные.")
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    """Обработчик для выхода из системы"""
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect('login') # Перенаправляем на страницу входа