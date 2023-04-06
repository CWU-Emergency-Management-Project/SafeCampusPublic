from django.db import models
from django.utils import timezone
from django.urls import reverse
import uuid
from django.db.models import Avg
from django.db.models.functions import ExtractWeekDay, ExtractHour
from datetime import timedelta, datetime
import pytz
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class Building(models.Model):
    """Model representing a building on campus"""

    TYPE = [
    ('Academic', 'Academic'),
    ('Apartment', 'Apartment'),
    ('Library', 'Library'),
    ('Sports Complex', 'Sports Complex'),
    ('Housing', 'Housing'),
    ('Student Services', 'Student Services'),
    ('Dining', 'Dining'),
    ('Administrative', 'Administrative'),
    ('Residence Hall', 'Residence Hall'),
    ('Other', 'Other'),
    ]

    TRAFFIC = [
    ('High', 'High'),
    ('Low', 'Low'),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    poly = models.CharField(max_length=1000,blank=True,null=True)
    lat = models.DecimalField(default=0.0,decimal_places=10,max_digits=14)
    long = models.DecimalField(default=0.0,decimal_places=10,max_digits=14)
    type = models.CharField(choices=TYPE,max_length=50,default="Other")
    traffic = models.CharField(choices=TRAFFIC,default="Low",max_length=4)
    floorPlanCapacity = models.PositiveSmallIntegerField(blank=True, null=True)
    registrarCapacity = models.PositiveSmallIntegerField(blank=True, null=True)
    deviceCount = models.PositiveSmallIntegerField(blank=True, null=True)
    estimateNumber = models.PositiveSmallIntegerField(blank=True, null=True)
    device_modified_at = models.DateTimeField(auto_now_add=True)
    estimate_modified_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    start_time = models.TimeField(auto_now_add=True)



    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.name
    
    # Overwrite save function to only update when the device count or estimate count changes
    def save(self, *args, **kwargs):

        # Setting date field to current date and start time to current time whenever model is saved
        tz = pytz.timezone(settings.TIME_ZONE)
        today = timezone.now().strftime('%Y-%m-%d')
        time = datetime.now(tz).strftime('%H')
        if self.date != today:
            self.date = today
        if self.start_time != time:
            self.start_time = time

        if self._state.adding:
            # new object, set the UUID and save timestamps
            self.uuid = uuid.uuid4()
        else:
            # object is existing, so check if the specific field has changed
            original = Building.objects.get(uuid=self.uuid)
            if original.deviceCount  != self.deviceCount :
                self.device_modified_at = timezone.now()
            if original.estimateNumber  != self.estimateNumber :
                self.estimate_modified_at = timezone.now()
        super().save(*args, **kwargs)

    def get_recent_count(self):
        counts = DeviceCount.objects.filter(building=self)
        if counts.exists():
            latest_count = counts.latest('timestamp_field')
            return latest_count.device_count
        else:
            return 0
        
    def get_count_last_modified(self):
        counts = DeviceCount.objects.filter(building=self)
        if counts.exists():
            latest_count = counts.latest('timestamp_field')
            return latest_count.timestamp_field
        else:
            return None
    
    def get_absolute_url(self):
        return reverse('building-detail', args=[str(self.pk)])
    #Function to set registrarCapacity to the correct count based on time and day
    def get_regCount(self):
        reg_data = RegData.objects.filter(
            name=self.name,
            date=self.date,
            start_time=self.start_time
        ).first()
        if reg_data:
            self.registrarCapacity = reg_data.count
            return reg_data.count
        else:
            return None
        
    def get_admin_url(self):
            content_type = ContentType.objects.get_for_model(self.__class__)
            return reverse('admin:%s_%s_change' % (content_type.app_label, content_type.model), args=(self.uuid,))
    
class DeviceCount(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    device_count = models.IntegerField()
    timestamp_field = models.DateTimeField(auto_now_add=True)

    def str(self):
        return str(self.id)

    def get_device_count_trends(building_id, weekday):
        # Query DeviceCount model for records matching the selected building and weekday
        device_counts = DeviceCount.objects.filter(
            building_id=building_id,
            timestamp_field__week_day=weekday
        )

        # Group device counts by hour and calculate average device count for each hour
        hour_averages = device_counts.annotate(
            hour=ExtractHour('timestamp_field')
        ).values('hour').annotate(
            average_device_count=Avg('device_count')
        )

        # Convert hour averages to a list of dictionaries
        trend_data = [{'hour': item['hour'], 'count': item['average_device_count']} for item in hour_averages]

        return trend_data
    
    def save(self, *args, **kwargs):
        # Run this code every time the model is saved, clears out rows that are roughly 3 months old.
        cut_off_date = timezone.now() - timedelta(days=30*3)  
        DeviceCount.objects.filter(timestamp_field__lt=cut_off_date).delete()
        super().save(*args, **kwargs)

class EmergencyModePollResult(models.Model):
    STATUS = [
    ('Safe', 'Safe'),
    ('Unsafe', 'Unsafe'),
    ('Not sure', 'Not sure'),
    ]

    status = models.CharField(choices=STATUS,max_length=50)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return str(self.id)

class EmergencyModeIndicator(models.Model):
    enabled = models.BooleanField(default=False)

    def _str_(self):
        """String for representing the Model object (in Admin site etc.)"""
        return str(self.id)
    
class RegData(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    count = models.PositiveSmallIntegerField(blank=True, null=True)
    
    def _str_(self):
        """String for representing the Model object (in Admin site etc.)"""
        return str(self.id)
