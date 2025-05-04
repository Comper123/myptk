from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.apps import apps
from .serializers import EquipmentTypeSerializer, EquipmentCreateSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from rest_framework import status

EquipmentType = apps.get_model('mysite', 'EquipmentType')
Equipment = apps.get_model('mysite', "Equipment")


# Create your views here.
class EquipmentTypesViewSet(viewsets.ModelViewSet):
    queryset = EquipmentType.objects.all()
    serializer_class = EquipmentTypeSerializer
    permission_classes = [IsAuthenticated]
    

class AddEquipmentView(APIView):
    permission_classes = [IsAuthenticated]
    
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request, format=None):
        serializer = EquipmentCreateSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Добавляем текущего пользователя как создателя
            equipment = serializer.save()
            
            return Response({
                'status': 'success',
                'data': serializer.data,
                'message': 'Оборудование успешно добавлено'
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': 'error',
            'errors': serializer.errors,
            'message': 'Ошибка валидации данных'
        }, status=status.HTTP_400_BAD_REQUEST)