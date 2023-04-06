from django.contrib import admin
from .models import Building
from .models import EmergencyModePollResult
from .models import EmergencyModeIndicator
from .models import RegData
# Register your models here.

admin.site.register(EmergencyModePollResult)
admin.site.register(EmergencyModeIndicator)
admin.site.register(RegData)

class BuildingAdmin(admin.ModelAdmin):
    fields =['name','type','traffic','floorPlanCapacity','registrarCapacity','lat','long','poly']
    exclude = ['deviceCount', 'estimateNumber']
    search_fields = ['name']
    list_filter = ['type','device_modified_at']

admin.site.register(Building, BuildingAdmin)

admin.site.site_header = 'SafeCampus Admin Dashboard'