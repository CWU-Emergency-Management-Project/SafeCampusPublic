# Generated by Django 4.1.6 on 2023-02-22 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0020_remove_building_id_alter_building_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building',
            name='traffic',
            field=models.CharField(choices=[('High', 'High'), ('Low', 'Low')], default='Low', max_length=4),
        ),
        migrations.AlterField(
            model_name='building',
            name='type',
            field=models.CharField(choices=[('Academic', 'Academic'), ('Apartment', 'Apartment'), ('Library', 'Library'), ('Sports Complex', 'Sports Complex'), ('Housing', 'Housing'), ('Student Services', 'Student Services'), ('Dining', 'Dining'), ('Administrative', 'Administrative'), ('Residence Hall', 'Residence Hall'), ('Other', 'Other')], max_length=50),
        ),
    ]
