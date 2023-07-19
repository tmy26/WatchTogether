# Generated by Django 4.2.3 on 2023-07-19 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_alter_room_room_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stream_link', models.URLField()),
                ('stream_room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.room')),
            ],
            options={
                'verbose_name_plural': 'Streams',
            },
        ),
    ]