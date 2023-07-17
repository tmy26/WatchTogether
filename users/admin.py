from django.contrib import admin
from .models import User, Room


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    search_fields = ('username',)

=======
    search_fields = ('user_name', 'email', 'first_name')
    list_display = ('user_name', 'email', 'password', 'first_name', 'last_name')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    search_fields = ('room_unique_id', 'room_name',)
    list_display = ('room_unique_id', 'room_name', 'room_password')
>>>>>>> main
