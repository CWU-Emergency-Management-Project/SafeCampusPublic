# Generated by Django 4.1.6 on 2023-02-22 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_alter_building_device_modified_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='device_modified_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='estimate_modified_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
