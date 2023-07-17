# Generated by Django 4.2.3 on 2023-07-13 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
    ]