# Generated by Django 4.1.6 on 2023-02-03 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_alter_building_estimatenumber_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmergencyModePollResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Safe', 'Safe'), ('Unsafe', 'Unsafe'), ('Not sure', 'Not sure')], max_length=50)),
                ('lat', models.DecimalField(blank=True, decimal_places=10, max_digits=12, null=True)),
                ('long', models.DecimalField(blank=True, decimal_places=10, max_digits=12, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
