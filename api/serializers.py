from rest_framework import serializers
from django.apps import apps

EquipmentType = apps.get_model('mysite', 'EquipmentType')
Equipment = apps.get_model('mysite', "Equipment")



class EquipmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentType
        fields = ['id', 'name', 'attributes_schema']
    
    
class EquipmentCreateSerializer(serializers.ModelSerializer):
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=EquipmentType.objects.all(),
        source='type',
        write_only=True
    )
    
    class Meta:
        model = Equipment
        fields = [
            'id', 'type_id', 'inventory_number', 
            'status', 'attributes', 'created_at'
        ]
        extra_kwargs = {
            'status': {'required': False, 'default': 'working'},
            'created_at': {'read_only': True}
        }
    
    def validate(self, data):
        equipment_type = data.get('type')
        attributes = data.get('attributes', {})
        
        if not equipment_type:
            raise serializers.ValidationError("Тип оборудования обязателен")
        
        # Валидация характеристик по схеме типа
        self.validate_attributes(equipment_type.attributes_schema, attributes)
        
        return data
    
    def validate_attributes(self, schema, attributes):
        for field, config in schema.items():
            if config.get('required', False) and field not in attributes:
                raise serializers.ValidationError(
                    {f"attributes.{field}": "Это поле обязательно"}
                )
            
            # Дополнительная валидация для списков
            if config.get('type') == 'list' and field in attributes:
                if not isinstance(attributes[field], list):
                    raise serializers.ValidationError(
                        {f"attributes.{field}": "Должен быть списком"}
                    )
                
                # Валидация элементов списка
                if 'fields' in config:
                    for item in attributes[field]:
                        for sub_field, sub_config in config['fields'].items():
                            if sub_config.get('required', False) and sub_field not in item:
                                raise serializers.ValidationError(
                                    {f"attributes.{field}.{sub_field}": "Это поле обязательно в списке"}
                                )
        
        return attributes