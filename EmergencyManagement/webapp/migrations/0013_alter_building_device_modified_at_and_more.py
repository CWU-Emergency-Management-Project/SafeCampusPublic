# Generated by Django 4.1.6 on 2023-02-22 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_rename_modified_at_building_device_modified_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='device_modified_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='building',
            name='estimate_modified_at',
            field=models.DateTimeField(),
        ),
    ]
