# Generated by Django 4.1.6 on 2023-02-16 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_wifidatacounts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wifidatacounts',
            old_name='count',
            new_name='deviceCount',
        ),
    ]