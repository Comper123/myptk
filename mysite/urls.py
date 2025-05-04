from django.urls import path 

from . import views


urlpatterns = [
    path('floor/<int:floor_id>', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cabinets/<str:cab>', views.cabinet_view, name="cabinet"),
    path('register/', views.register_view, name="register"),
    path('confirm_user/<int:user_id>/', views.confirm_user_ajax, name='confirm_user_ajax'),
    path('addequipment/', views.addEquipment, name="addequipment")
]
