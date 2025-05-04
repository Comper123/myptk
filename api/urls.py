from django.urls import path 

from . import views


urlpatterns = [
    path("equipmenttypes", views.EquipmentTypesViewSet.as_view({'get': 'list'})), # для списка типов оборудования
    path("addequipment/", views.AddEquipmentView.as_view())
]
