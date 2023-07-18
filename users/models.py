from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.conf import settings
import uuid



class User(AbstractUser):

    username = models.CharField(max_length=20, blank=False, unique=True, default='asd')
    email = models.EmailField(blank=False)
    
    def __str__(self) -> str:
        return self.username
    
    @property
    def token(self):
        token_obj = Token.objects.filter(user=self).first()
        if token_obj:
            return token_obj.key


# Rooms model
class Room(models.Model):
    class Meta:
        verbose_name_plural = "Rooms"
        #git
    
    # Room properties
    room_unique_id =  models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)

    room_name = models.CharField(max_length=100, blank=False)
    room_password = models.CharField(max_length=50, blank=False)

    #TODO: If the owner user is deleted, CASCADE deletes the Room, assign a room owner
    #TODO: Make room default name -> "<Username>'s room", blank=False

