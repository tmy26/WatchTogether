#chat_app/models.py
from django.db import models
from wt_mobile.models import Room, User

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return self.content
