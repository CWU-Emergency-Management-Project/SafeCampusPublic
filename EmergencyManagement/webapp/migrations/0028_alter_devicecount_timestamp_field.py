# Generated by Django 4.1.6 on 2023-02-26 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0027_devicecount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devicecount',
            name='timestamp_field',
            field=models.DateTimeField(),
        ),
    ]
