# Generated by Django 4.1.6 on 2023-02-22 21:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0016_alter_building_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
