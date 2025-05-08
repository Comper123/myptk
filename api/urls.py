from django.urls import path 

from . import views


urlpatterns = [
    # Пути для api
    path("equipmenttypes", views.EquipmentTypesViewSet.as_view({'get': 'list'})), # для списка типов оборудования
    path("addequipment/", views.AddEquipmentView.as_view()),
    path('rooms', views.RoomsView.as_view()),
    path('equipment/<int:equipment_id>', views.EqupmentView.as_view()),
    path('moveequipment', views.EquipmentMoveView.as_view()),
    path('discardequipment', views.EquipmentDiscardView.as_view())
]
