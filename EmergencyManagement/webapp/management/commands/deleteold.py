from django.core.management.base import BaseCommand
from webapp.models import DeviceCount, Building
import uuid

class Command(BaseCommand):
    help = 'Updates existing MyModel entries to use UUID primary key'
    def handle(self, *args, **options):
        null_objects = DeviceCount.objects.all()

# Delete all objects with null field
        for obj in null_objects:
            obj.building = Building.objects.get(uuid='3fe45340ce594e7596f578a3519a3adb')
            obj.save() 
        #print(DeviceCount.get_device_count_trends('a9f31c7419c5430cbef786bea5b595b9',4));
        #print(DeviceCount.get_device_count_trends('a9f31c7419c5430cbef786bea5b595b9',5));    