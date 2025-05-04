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