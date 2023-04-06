# Generated by Django 4.1.5 on 2023-01-25 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building',
            name='location',
        ),
        migrations.AddField(
            model_name='building',
            name='lat',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=12),
        ),
        migrations.AddField(
            model_name='building',
            name='long',
            field=models.DecimalField(decimal_places=10, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='building',
            name='type',
            field=models.CharField(choices=[('Hall', 'Hall'), ('Recreation', 'Recreation'), ('Library', 'Library'), ('Sports Complex', 'Sports Complex'), ('Housing', 'Housing'), ('Other', 'Other')], max_length=50),
        ),
    ]