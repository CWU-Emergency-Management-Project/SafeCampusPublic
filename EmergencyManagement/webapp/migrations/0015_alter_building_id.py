# Generated by Django 4.1.6 on 2023-02-22 20:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0014_alter_building_device_modified_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
