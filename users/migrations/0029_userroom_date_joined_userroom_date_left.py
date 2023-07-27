# Generated by Django 4.2.2 on 2023-07-24 15:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_alter_room_room_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userroom',
            name='date_joined',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='userroom',
            name='date_left',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]