from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import JSONField

from . models import (
    Floor, 
    Room, 
    User, 
    CabinetPhoto,
    Equipment,
    EquipmentType
)


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    pass 


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass 


# Регистрация модели пользователя
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("first_name", "last_name", "groups_display", 'last_login', 'confirm_button')
    
    def confirm_button(self, obj):
        if obj.last_login is None and not obj.is_active:
            #  Собираем URL для AJAX запроса (важно)
            url = reverse('confirm_user_ajax', args=[obj.pk])  #  Используем reverse
            return format_html(
                '<button class="button confirm-user-button" data-url="{}">Подтвердить</button>',
                url,
            )
        return '-'

    confirm_button.short_description = 'Подтвердить'
    
    fieldsets = BaseUserAdmin.fieldsets
    readonly_fields = ('last_login',)
    
    def get_queryset(self, request):
        # Include last_login and groups in the queryset. Required for the filter and display.
        qs = super().get_queryset(request)
        return qs
    
    class Media:
        js = ('/static/js/userConfirm.js',)
        

# Админка изображений кабинета
@admin.register(CabinetPhoto)
class RoomPhotoAdmin(admin.ModelAdmin):
    list_display = ("image", "upload_at")


# Админка типов оборудования
@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }


# Админка для оборудования
@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("inventory_number", "type_name", "is_active", "room")
    
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }