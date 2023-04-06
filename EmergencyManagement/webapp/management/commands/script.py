from django.core.management.base import BaseCommand
from webapp.models import Building, DeviceCount
import uuid
import json
from datetime import datetime, timedelta
from random import randint
import pytz
from django.utils import timezone

class Command(BaseCommand):
    help = 'Updates existing MyModel entries to use UUID primary key'

    def handle(self, *args, **options):
        # Open the GeoJSON file

        # Get the building object for which to create device count data
        buildings = Building.objects.all()

        

        # Loop over 48 intervals of 30 minutes each
        for building in buildings:
            # Define the end time of the interval as 30 minutes after the start time
            start_time = datetime(2023, 2, 27, 0, 0, 0)
            device_count = randint(50, 400)
            print(building.name)
            print(device_count)
            # Create a new DeviceCount object with the generated data
            new_count = DeviceCount(
                building=building,
                device_count=device_count,
                timestamp_field=start_time,
            )
            new_count.save()
            
            # Update the start time for the next interval
            #start_time = end_time