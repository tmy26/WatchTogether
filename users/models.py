from django.db import models
from django.conf import settings

# Create your models here.

class User(models.Model):

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