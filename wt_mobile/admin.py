from django.contrib import admin
from .models import User, Room, Stream


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('username', 'password', 'email')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    search_fields = ('unique_id', 'name',)
    list_display = ('unique_id', 'name', 'password',)


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    search_fields = ('link', 'assigned_room',)
    list_display = ('link', 'assigned_room',)
    