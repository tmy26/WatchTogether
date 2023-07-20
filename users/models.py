from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    username = models.CharField(max_length=20, blank=False, unique=True)
    email = models.EmailField(blank=False)
    
    def __str__(self) -> str:
        return self.username


# Rooms model
class Room(models.Model):
    class Meta:
        verbose_name_plural = "Rooms"
    
    # Room properties
    room_unique_id = models.CharField(max_length=100, blank=True, unique=True)
    room_name = models.CharField(max_length=100, blank=False)
    room_password = models.CharField(max_length=50, blank=True)

    #TODO: If the owner user is deleted, CASCADE deletes the Room