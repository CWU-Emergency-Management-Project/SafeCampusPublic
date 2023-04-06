import os
import sys
import django
from django.conf import settings

# Connect to Django project
sys.path.append('I:\School\CS481\Emergency-Management\EmergencyManagement')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmergencyManagement.settings')
django.setup()

# import the database connection from django
from django.db import connection

from webapp.models import DeviceCount

def update_device_counts():
    # Retrieve all DeviceCount objects
    device_counts = DeviceCount.objects.all()

    # Loop through each DeviceCount object and set device_count to 0
    for device_count in device_counts:
        device_count.device_count = 0
        device_count.save()
        print("Updated device count for building: ")
        print(device_count.id)

update_device_counts()
