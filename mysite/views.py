from django.shortcuts import render


# Create your views here.
def index(request, floor_id):
    """Метод отображения главной страницы"""
    data = {
        
    }
    return render(request, "index.html", data)