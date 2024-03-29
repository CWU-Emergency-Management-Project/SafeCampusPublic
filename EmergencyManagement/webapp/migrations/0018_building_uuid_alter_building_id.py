# Generated by Django 4.1.6 on 2023-02-22 21:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0017_alter_building_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='uuid',
            field=models.UUIDField(blank=True, default=uuid.uuid4, null=True),
        ),
        migrations.AlterField(
            model_name='building',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
