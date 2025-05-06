from rest_framework import serializers
from django.apps import apps

EquipmentType = apps.get_model('mysite', 'EquipmentType')
Equipment = apps.get_model('mysite', "Equipment")
Room = apps.get_model('mysite', "Room")


class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ['id', 'name', 'attributes_schema']
    

    
    
class EquipmentCreateSerializer(serializers.ModelSerializer):
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        source='room',  # Указываем, что записываем в поле room модели
        write_only=True,
        required=False,  # Если кабинет может быть не указан
        allow_null=True  # Разрешаем null значение
    )
    
    class Meta:
        model = Equipment
        fields = ['type', 'room_id', 'inventory_number', 'attributes']
    
    def validate(self, attrs):
        typeName = attrs.get('type')
        attributes = attrs.get('attributes', {})
        
        if not typeName:
            raise serializers.ValidationError(
                {"type": "Тип оборудования обязателен"}
            )
            
        equipment_type = EquipmentType.objects.get(name=typeName)
        
        
        # Валидация атрибутов по схеме типа
        self._validate_attributes(equipment_type.attributes_schema, attributes)
        
        return attrs
    
    def validate_attributes(self, value):
        """
        Переопределяем базовую валидацию
        """
        if not isinstance(value, dict):
            raise serializers.ValidationError("Атрибуты должны быть в виде словаря")
        return value
    
    def _validate_attributes(self, schema, attributes):
        """
        Валидация характеристик оборудования по схеме типа
        """
        errors = {}
        # Проверка обязательных полей
        for field, config in schema.items():
            if config.get('required', False) and field not in attributes:
                errors[field] = "Это поле обязательно"
            
            # Валидация списков
            if config.get('type') == 'list' and field in attributes:
                if not isinstance(attributes[field], list):
                    errors[field] = "Должен быть списком"
                elif 'fields' in config:
                    for i, item in enumerate(attributes[field]):
                        for sub_field, sub_config in config['fields'].items():
                            if sub_config.get('required', False) and sub_field not in item:
                                errors[f"{field}[{i}].{sub_field}"] = "Это поле обязательно в списке"
        
        if errors:
            raise serializers.ValidationError({"attributes": errors})