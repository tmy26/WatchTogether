# Generated by Django 4.2.2 on 2023-07-19 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_alter_room_room_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
