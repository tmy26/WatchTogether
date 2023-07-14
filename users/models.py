from django.db import models

# Create your models here.

class User(models.Model):

    class Meta:
        verbose_name_plural = "Users"

    user_name = models.CharField(max_length=15, blank=False)
    email = models.CharField(max_length=30, blank=False)
    password = models.CharField(max_length=50, blank=False)
    first_name = models.CharField(max_length=20, blank=False)
    last_name = models.CharField(max_length=50, blank=True)
    