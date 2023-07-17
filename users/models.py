from django.db import models
<<<<<<< HEAD
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
=======
from django.conf import settings

>>>>>>> main
# Create your models here.

class User(AbstractUser):

<<<<<<< HEAD
    username = models.CharField(max_length=20, blank=False, unique=True, default='asd')
    email = models.EmailField(blank=False)
    
    def __str__(self) -> str:
        return self.username
    
    @property
    def token(self):
        token_obj = Token.objects.filter(user=self).first()
        if token_obj:
            return token_obj.key
=======
    class Meta:
        verbose_name_plural = "Users"

    user_name = models.CharField(max_length=15, blank=False)
    email = models.CharField(max_length=30, blank=False)
    password = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=50, blank=True)


# Rooms model
class Room(models.Model):
    class Meta:
        verbose_name_plural = "Rooms"
    
    # Room properties
    room_unique_id = models.CharField(max_length=100, blank=True, unique=True)
    room_name = models.CharField(max_length=100, blank=False)
    room_password = models.CharField(max_length=50, blank=True)

    #TODO: If the owner user is deleted, CASCADE deletes the Room
>>>>>>> main
