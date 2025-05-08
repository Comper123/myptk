from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.apps import apps
from .serializers import (
    EquipmentTypeSerializer, 
    EquipmentCreateSerializer,
    EquipmentSerializer
)
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status

EquipmentType = apps.get_model('mysite', 'EquipmentType')
Equipment = apps.get_model('mysite', "Equipment")
Room = apps.get_model('mysite', "Room")


# Create your views here.
class EquipmentTypesViewSet(viewsets.ModelViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    permission_classes = [IsAuthenticated]
    

class AddEquipmentView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = EquipmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            equipment = serializer.save()
            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class RoomsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response([
            {
                "id": r.id,
                "name": r.name
            }
            for r in Room.objects.all()
        ], status=status.HTTP_200_OK)


class EqupmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, equipment_id):
        eq = Equipment.objects.get(id=equipment_id)
        return Response({
            "id": eq.id,
            "inventory_number": eq.inventory_number,
            "name": eq.type.name + " " + str(eq.inventory_number),
            "room_id": eq.room.id
        }, status=status.HTTP_200_OK)
        

class EquipmentMoveView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        equipment = Equipment.objects.get(id=request.data["eq_id"])
        room = Room.objects.get(id=request.data["room_id"])
        equipment.room = room
        equipment.save(moved_by=request.user)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class EquipmentDiscardView(APIView):
    """Обработчик списания оборудования"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        equipment = Equipment.objects.get(id=request.data["eq_id"])
        equipment.is_active = False
        equipment.save(discard_by=request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)