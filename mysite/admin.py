from django.contrib import admin

from . models import Floor, Room, User
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

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
            url = reverse('confirm_user', args=[obj.pk]) 
            return format_html(
                '<a class="button" href="{}">Подтвердить</a>',
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