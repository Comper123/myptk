from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404

from . forms import LoginForm
from . import models
import json


@csrf_protect
def save_cabinet(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data['name']
            coords = data['coords']
            floor_id = int(data['floor_id'])
            
            coords_string = ' '.join([f"{coord['x']},{coord['y']}" for coord in coords])
            #  Тут получаем floor id. Как вы это делаете - зависит от вашей логики
            #  например, из сессии: floor_id = request.session.get('floor_id')

            floor = get_object_or_404(models.Floor, pk=floor_id) #Floor нужно импортировать вверху
            room = models.Room(name=name, coords=coords_string, floor=floor)
            room.save()
            return JsonResponse({'status': 'success', 'message': 'Кабинет сохранен', 'room_id': room.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


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