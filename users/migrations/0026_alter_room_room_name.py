# Generated by Django 4.2.3 on 2023-07-26 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_merge_20230725_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='room_name',
            field=models.CharField(blank=True, max_length=101, null=True),
        ),
    ]
