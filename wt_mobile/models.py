from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    username = models.CharField(max_length=20, blank=False, unique=True)
    email = models.EmailField(blank=False)
    
    def __str__(self) -> str:
        return self.username


class Room(models.Model):
    class Meta:
        verbose_name_plural = "Rooms"
    
    unique_id =  models.CharField(
        max_length=8,
        primary_key=True,
        editable=False,
        unique=True)
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=101, null=True, blank=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    users = models.ManyToManyField(User, through='UserRoom', related_name='users_room')

    def __str__(self) -> str:
        return str(self.name)


class UserRoom(models.Model):
    class Meta:
        db_table = "%s_%s" % (__package__, "room_participants")

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, blank=False)
    date_joined = models.DateField(blank=True, default=now)


# class Stream(models.Model):
#     class Meta:
#         verbose_name_plural = "Streams"
 
#     link = models.URLField(blank=True, null=True, default='https://www.youtube.com/watch?v=71Gt46aX9Z4')
#     assigned_room = models.OneToOneField(Room, on_delete=models.CASCADE)


# class StreamHistory(models.Model):
#     """Store all the links played within the room"""
#     class Meta:
#         verbose_name_plural = "StreamHistories"
#         db_table = "%s_%s" % (__package__, "stream_history")
    
#     stream = models.ForeignKey(Stream, on_delete=models.CASCADE, null=True, blank=False)
#     time_when_played = models.CharField(max_length=30, blank=True)
#     link = models.URLField(blank=True, null=True)
    