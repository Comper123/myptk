from django.urls import path 

from . import views


urlpatterns = [
    path('floor/<int:floor_id>', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('save_cabinet/', views.save_cabinet, name='save_cabinet'),
]
