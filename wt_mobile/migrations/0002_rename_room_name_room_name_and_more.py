# Generated by Django 4.2.2 on 2023-07-31 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wt_mobile', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='room_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='room_owner',
            new_name='owner',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='room_password',
            new_name='password',
        ),
        migrations.RenameField(
            model_name='room',
            old_name='room_unique_id',
            new_name='unique_id',
        ),
    ]