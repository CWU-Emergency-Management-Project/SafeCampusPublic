from datetime import datetime
import time
import pytz
import os
import sys
import django
from django.conf import settings
import logging

#Set up the Django environment
#sys.path.append('set to where manage.py is stored')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmergencyManagement.settings')
#Can be commented out when running in thread
django.setup()

from webapp.models import Building
tz = pytz.timezone(settings.TIME_ZONE)
logging.basicConfig(level=logging.DEBUG)

#Function to get the current day and return a percentage of the total number value
def getDay(totalNum):
    day = datetime.now(tz).weekday()
    if day == 0:
        return -0.25 * totalNum
    elif day in (1, 2, 3):
        return 0.25 * totalNum
    elif day == 4:
        return 0.5 * totalNum
    elif day in (5, 6):
        return -0.8 * totalNum
    else:
        return 0
    

#Function to get the current hour and then return a percentage of the total number
def getTime(totalNum, fData):
    curtime = datetime.now(tz).strftime("%H")
    if curtime in ("6", "7", "8", "9"):
        return -0.1 * totalNum
    elif curtime in ("12", "13"):
        return 0.1 * totalNum
    elif curtime in ("10", "11", "14", "15"):
        return 0.05 * totalNum
    elif curtime in ("16", "17"):
        return -0.05 * totalNum
    elif curtime == "18":
        return 0
    elif curtime in ("19", "20"):
        return 0.05 * (totalNum - fData)
    else:
        return fData * 0.05

#Function that takes a string as input and returns a percentage of the total number
def getTraffic(totalNum, level):
        if level == "High":
            return 0.1 * totalNum
        elif level == "Low":
            return -0.05 * totalNum
        else:
            return 0

#Main function to get final estimation
def getEst():
    #while True:
        for obj in Building.objects.all():
            fData = obj.floorPlanCapacity
            obj.get_regCount()
            regData = obj.registrarCapacity
            if fData == None:
                fData = 0
            if regData == None:
                regData = 0
            totalNum = fData + regData
            level = obj.traffic
            DoW = getDay(totalNum)
            AvgT = getTraffic(totalNum, level)
            ToD = getTime(totalNum,fData)
            
            finalNum = totalNum + ToD + DoW + AvgT    
            obj.estimateNumber = finalNum
            obj.save()
        #logging.debug("Working")
        #time.sleep(3600)

getEst()
