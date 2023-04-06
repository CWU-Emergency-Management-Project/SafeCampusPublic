# Generated by Django 4.1.6 on 2023-02-22 21:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0018_building_uuid_alter_building_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]
