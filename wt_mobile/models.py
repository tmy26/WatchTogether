from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
import shortuuid


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
    unique_id =  models.CharField(
        max_length=8,
         primary_key=True,
         default=shortuuid.ShortUUID().random(length=6),
         editable=False,
         unique=True)
    
    # delete rooms, if the related user is also deleted
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # Room name and password
    name = models.CharField(max_length=101, null=True, blank=True)
    password = models.CharField(max_length=50, blank=True, null=True)

    users = models.ManyToManyField(User, through='UserRoom', related_name='users_room')

    def __str__(self) -> str:
        return str(self.name)


# Join User-Room model
class UserRoom(models.Model):
    class Meta:
        # Set db name from default to 'room_participants'
        db_table = "%s_%s" % (__package__, "room_participants")

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, blank=False)
    room_name = models.CharField(max_length=101)
    date_joined = models.DateField(blank=True, default=now)


# Stream
class Stream(models.Model):
    
    class Meta:
        verbose_name_plural = "Streams"
 
    # Stream property
    link = models.URLField(blank=True, null=True, default=None)
    assigned_room = models.OneToOneField(Room, on_delete=models.CASCADE)
    