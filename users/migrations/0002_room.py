# Generated by Django 4.1.7 on 2023-07-14 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=100)),
                ('room_password', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Rooms',
            },
        ),
    ]