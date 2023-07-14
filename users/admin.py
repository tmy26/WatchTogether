from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('user_name', 'email', 'first_name')
    list_display = ('user_name', 'email', 'password', 'first_name', 'last_name')
