# Generated by Django 4.1.6 on 2023-02-16 00:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_alter_building_lat_alter_building_long_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WifiDataCounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.building')),
            ],
        ),
    ]