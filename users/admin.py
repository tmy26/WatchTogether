from django.contrib import admin
from .models import User, Room


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'password', 'email')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    search_fields = ('room_unique_id', 'room_name', 'room_owner')
    list_display = ('room_unique_id', 'room_name', 'room_password', 'room_owner')
