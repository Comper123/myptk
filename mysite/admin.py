from django.contrib import admin

from . models import Floor, Room


@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    pass 


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass 