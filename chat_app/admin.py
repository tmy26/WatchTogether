from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    search_fields = ('content', 'timestamp', 'room_id', 'sender_id')
    list_display = ('content', 'timestamp', 'room_id', 'sender_id')
