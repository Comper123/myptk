from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.core.cache import cache

from . forms import LoginForm, RegisterForm, EquipmentFilterForm
from . import models


def index(request, floor_id):
    """
    Обработчик главной страницы
    """
    floor = models.Floor.objects.get(name=floor_id)
    data = {
        "floor": floor,
        "floors": models.Floor.objects.all(),
        "width": floor.image.width,
        "height": floor.image.height
    }
    return render(request, "floor.html", data)


def register_view(request):
    """
    Обработчик регистрации в системе
    """
    data = {}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            return redirect("/login") # Перенаправляем на вход
        else:
            data["message"] = "Ошибка валидации"
    else:
        form = RegisterForm()
    data['form'] = form
    return render(request, 'account/register.html', data)
    
    
def login_view(request):
    """
    Обработчик страницы авторищзации в системе
    """
    data = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Используем встроенный login Django
            messages.success(request, f"Вы успешно вошли как {user.username}!")
            return redirect("/floor/1") # Перенаправляем на главную
        else:
            data["message"] = "Ошибка валидации"
    else:
        form = LoginForm()
    data['form'] = form
    return render(request, 'account/login.html', data)


def logout_view(request):
    """
    Обработчик для выхода из системы
    """
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect('login') # Перенаправляем на страницу входа


def cabinet_view(request, cab):
    # Получаем текущие параметры GET-запроса
    get_params = request.GET.copy()
    
    # Удаляем параметр page из копии (чтобы не дублировался)
    if 'page' in get_params:
        del get_params['page']
    
    # Формируем строку параметров для пагинации
    params = get_params.urlencode()
    
    room = models.Room.objects.get(name=cab)
    context = {
        'room': room
    }
    queryset = models.Equipment.objects.filter(room=room)
    form = EquipmentFilterForm(request.GET)
    
    if form.is_valid():
        data = form.cleaned_data
        
        # Фильтрация по поисковому запросу
        if data['search']:
            queryset = queryset.filter(
                # models.models.Q(name__icontains=data['search']) |
                models.models.Q(inventory_number__icontains=data['search'])
            )
        
        # Фильтрация по типу
        if data['equipment_type']:
            eq_type = models.EquipmentType.objects.get(name=data['equipment_type'])
            queryset = queryset.filter(type=eq_type)
        
        # Фильтрация по статусу
        if data['status']:
            queryset = queryset.filter(status=data['status'])
        
        # Фильтрация по дате
        if data['purchase_date_from']:
            queryset = queryset.filter(purchase_date__gte=data['purchase_date_from'])
        
        if data['purchase_date_to']:
            queryset = queryset.filter(purchase_date__lte=data['purchase_date_to'])
    
    # Пагинация
    paginator = Paginator(queryset, 10)  # 10 элементов на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['page_obj'] = page_obj
    context['form'] = form
    context['query_params'] = params
    
    return render(request, "cabinet.html", context)



@csrf_exempt # Отключаем CSRF для этого view
def confirm_user_ajax(request, user_id):
    """
    Обработчик AJAX для подтверждения пользователя.
    """
    if request.method == 'POST':
        try:
            User = get_user_model()  # Получаем модель User
            user = User.objects.get(pk=user_id)  #  Получаем пользователя по ID

            if user.last_login is None and not user.is_active:
                user.is_active = True  #  Активируем пользователя
                user.save()

                return JsonResponse({'status': 'success', 'message': 'Пользователь подтвержден.'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Пользователь уже подтвержден.'}, status=400) #  400 -  Bad Request

        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Пользователь не найден.'}, status=404)  #  404 - Not Found
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500) # 500 - Internal Server Error

    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса.'}, status=405) # 405 - Method Not Allowed


def addEquipment(request):
    """
    Обработчик страницы добавления фильма
    """
    return render(request, "addequipment.html")