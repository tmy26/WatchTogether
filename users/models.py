from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
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
    
    # Room properties
    room_unique_id =  models.UUIDField(
         primary_key=True,
         default=uuid.uuid4,
         editable=False)
    
    # delete rooms, if the related user is also deleted
    room_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    room_name = models.CharField(max_length=100, blank=True, null=True)
    room_password = models.CharField(max_length=50, blank=True, null=True)

    #TODO: Make room default name -> "<Username>'s room", blank=False

    def __str__(self) -> str:
        return self.room_name


# Stream
class Stream(models.Model):
    
    class Meta:
        verbose_name_plural = "Streams"
 
    # Stream property
    link = models.URLField()
    assigned_room = models.OneToOneField(Room, on_delete=models.CASCADE)