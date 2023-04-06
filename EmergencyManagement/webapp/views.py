from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import BuildingSerializer, EmergencyModePollResultSerializer, EmergencyModeIndicatorSerializer, DeviceCountSerializer
from .models import Building, EmergencyModePollResult, EmergencyModeIndicator, DeviceCount, RegData
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models.functions import ExtractWeekDay, ExtractHour
from .forms import AlertForm, uploadFileForm, uploadCSVForm
from django.db.models import Avg
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET
import openpyxl
from datetime import datetime
import requests
from django.contrib import messages
import os
import csv
import sys
#import pandas as pd
#import tkinter as tk
#from tkinter import filedialog
from django.db import connection
from django.db import transaction
# Create your views here.

#Function to open an excel file and then fill the RegData DBs corresponding fields
def process_data(f):
    workbook = openpyxl.load_workbook(f) 
    worksheet = workbook.active
    for row in worksheet.iter_rows(min_row=2, values_only=True):
        reg_data = RegData.objects.update_or_create(
            name=row[0],
            date=row[1],
            start_time=row[2],
            count=row[3]
        )

@login_required
def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

@login_required
def buildingsList(request):
    """View function for building list page"""
    buildings = Building.objects.all()

    context = {
        'buildings': buildings
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'list.html', context=context)

@login_required
def buildingDetails(request, building_id):
    buildingObj = get_object_or_404(Building, uuid=building_id)

    context = {
        'building': buildingObj,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'details.html', context=context)

@login_required
def results(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    results = EmergencyModePollResult.objects.all()

    context = {
        'results': results
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'results.html', context=context)

@login_required
def map(request):
    """View function for map page of site"""
    if request.method == 'POST':
        if 'file' in request.FILES:
            form = uploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                try: 
                    process_data(request.FILES['file'])
                    messages.success(request, 'Updated registrar data')
                    return redirect('map')
                except:
                    messages.error(request, 'There was an error processing your form.')
                    return redirect('map')
            else:
                return redirect('map')
        elif 'csvFile' in request.FILES:
            csvForm = uploadCSVForm(request.POST, request.FILES)
            if csvForm.is_valid():
                try: 
                    getRaveData(request.FILES['csvFile'])
                    messages.success(request, 'Updated rave alert data')
                    return redirect('map')
                except:
                    messages.error(request, 'There was an error processing your csv form.')
                    return redirect('map')
            else:
                return redirect('map')
        elif 'way_id' in request.POST:
            # Get the form data from the POST request
            way_id = request.POST['way_id']
            # Fetch additional building data from the Overpass API
            overpass_url = "http://overpass-api.de/api/interpreter"
            query = (
                f'[out:json][timeout:25];'
                f'way({way_id});'
                f'out center;'
                f'out geom;'
                f'>;'
            )
            response = requests.get(overpass_url, params={'data': query}).json()
            name = response['elements'][0]['tags'].get('name', '')
            center = response['elements'][0]['center']
            geometry = response['elements'][1]['geometry']
            coord_list = [[coord["lat"], coord["lon"]] for coord in geometry]
            print(name)
            print(center["lat"])
            print(center["lon"])
            print(coord_list)
            # Create a new Building object and save it to the database
            building = Building.objects.create(name=name, poly=coord_list, lat=center["lat"], long=center["lon"])
            messages.success(request, 'Added new building: ' + str(name))
            return redirect('map')
        else:
            return redirect('map')
    else:
        # Generate counts of some of the main objects
        buildings = Building.objects.all()
        emergIndicator = EmergencyModeIndicator.objects.get()
        results = EmergencyModePollResult.objects.all()
        building_types = list(Building.objects.values_list('type', flat=True).distinct())
        form = uploadFileForm()     
        csvForm = uploadCSVForm()

        context = { 
            'buildings': buildings,
            'emergIndicator' : emergIndicator,
            'results' : results,
            'types': building_types,
            'form': form,
            'csvForm' : csvForm
        }

        # Render the HTML template map.html with the data in the context variable
        return render(request, 'map.html', context=context)

@login_required
def emergMap(request):
    """View function for map page of site"""

    # Generate counts of some of the main objects
    buildings = Building.objects.all()
    emergIndicators = EmergencyModeIndicator.objects.all()
    results = EmergencyModePollResult.objects.all()
    
    context = { 
        'buildings': buildings,
        'emergIndicators' : emergIndicators,
        'results' : results
    }

    # Render the HTML template map.html with the data in the context variable
    return render(request, 'emerg_map.html', context=context)

#View to run functionality of upload registrar data button
@login_required
def upload_file(request):
    if request.method == 'POST':
        form = uploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            process_data(request.FILES['file'])
            return HttpResponseRedirect('/form/')
    else:
        form = uploadFileForm()
    return render(request, 'form.html', {'form': form})
    

def alert(request):
    if request.method == 'POST':
        form = AlertForm(request.POST)
        if form.is_valid():
            alert = form.save(commit=False)
            if request.POST.get('send_location') == 'on' and (request.POST.get('lat') != ''):
                alert.lat = request.POST.get('lat')
                alert.long = request.POST.get('long')
            alert.save()
            return render(request, 'alertsuccess.html')
    else:
        form = AlertForm()
    return render(request, 'alert.html', {'form': form})
    
'''
class MapView(viewsets.ModelViewSet):
    """
    API endpoint that allows map to be created
    """
    template_name = "map.html"
'''

@login_required
def getDeviceCountJSON(request, building_id, weekday):
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

    return JsonResponse({'trend_data': trend_data})

def getEmergencyPollJSON(request):
    results = EmergencyModePollResult.objects.all()
    data = {'results': list(results.values())}
    return JsonResponse(data)

@login_required
@require_GET
def getBuildingFilterJSON(request):
    selected_types = request.GET.get('type', '')
    buildings_data = []
    if len(selected_types) > 0:
        if 'All' in selected_types.split(','):
            selected_types = Building.objects.values_list('type', flat=True).distinct()
        else:
            selected_types = selected_types.split(',')
        buildings = Building.objects.filter(type__in=selected_types)
        for building in buildings:
            buildings_data.append({
                'id': building.uuid,
                'name': building.name,
                'estimateNumber': building.estimateNumber,
                'lat': building.lat,
                'long': building.long,
                'type': building.type,
                'poly': building.poly,
                'url': building.get_absolute_url(),
                'deviceCount': building.get_recent_count(),
                'device_modified_at': building.get_count_last_modified()
                # add other fields as needed
            })
    return JsonResponse(buildings_data, safe=False)

@login_required
@require_GET
def getSearchJSON(request):
    query = request.GET.get('q')
    buildings_data = []
    if query:
        buildings = Building.objects.filter(name__icontains=query)
        for building in buildings:
            buildings_data.append({
                'id': building.uuid,
                'name': building.name,
                'estimateNumber': building.estimateNumber,
                'lat': building.lat,
                'long': building.long,
                'type': building.type,
                'poly': building.poly,
                'url': building.get_absolute_url(),
                'deviceCount': building.get_recent_count(),
                'device_modified_at': building.get_count_last_modified()
                # add other fields as needed
            })
        return JsonResponse(buildings_data, safe=False)
    else:
        buildings = Building.objects.all()
        for building in buildings:
            buildings_data.append({
                'id': building.uuid,
                'name': building.name,
                'estimateNumber': building.estimateNumber,
                'lat': building.lat,
                'long': building.long,
                'type': building.type,
                'poly': building.poly,
                'url': building.get_absolute_url(),
                'deviceCount': building.get_recent_count(),
                'device_modified_at': building.get_count_last_modified()
                # add other fields as needed
            })
        return JsonResponse(buildings_data, safe=False)

@login_required
def deleteSMSPollData(request):
    EmergencyModePollResult.objects.all().delete()


def toggle_emergency_indicator(request):
    print("Toggle Emergency Mode Reached")
    if request.method == 'POST':
        csrf_token = request.POST.get('csrfmiddlewaretoken')
        enabled = request.POST.get('enabled')
        indicator = get_object_or_404(EmergencyModeIndicator, id=1)
        if enabled == 'true':
            indicator.enabled = True
            indicator.save()
            return JsonResponse({'success': True})
        elif enabled == 'false':
            with transaction.atomic():
                deleteSMSPollData(request)
                indicator.enabled = False
                indicator.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid "enabled" parameter value'})
    else:
        return JsonResponse({'error': 'Invalid HTTP method'})

@login_required
def addBuilding(request):
    if request.method == 'POST':
        # Get the form data from the POST request
        way_id = request.POST['way_id']
        # Fetch additional building data from the Overpass API
        overpass_url = "http://overpass-api.de/api/interpreter"
        query = (
            f'[out:json][timeout:25];'
            f'way({way_id});'
            f'out center;'
            f'out geom;'
            f'>;'
        )
        response = requests.get(overpass_url, params={'data': query}).json()
        name = response['elements'][0]['tags'].get('name', '')
        center = response['elements'][0]['center']
        geometry = response['elements'][1]['geometry']
        coord_list = [[coord["lat"], coord["lon"]] for coord in geometry]
        print(name)
        print(center["lat"])
        print(center["lon"])
        print(coord_list)
        # Create a new Building object and save it to the database
        building = Building.objects.create(name=name, poly=coord_list, lat=center["lat"], long=center["lon"])
        return redirect('map')
    else:
        return render(request, 'addBuilding.html')

@login_required
def getBuildingSearchJSON(request):
    if request.method == 'GET' and 'way_id' in request.GET:
        try:
            # Get the way ID from the query string
            way_id = request.GET['way_id']
            # Construct the Overpass query string
            query = (
                f'[out:json][timeout:25];'
                f'way({way_id});'
                f'out center;'
                f'out geom;'
                f'>;'
            )
            # Construct the URL for the Overpass API request
            overpass_url = "http://overpass-api.de/api/interpreter"
            api_url = f"{overpass_url}"
            # Send the API request and get the response
            response = requests.get(api_url, params={'data': query}).json()
            # Extract the building name, center point, and geometry
            name = response['elements'][0]['tags'].get('name', '')
            center = response['elements'][0]['center']
            geometry = response['elements'][1]['geometry']
            coord_list = [[coord["lat"], coord["lon"]] for coord in geometry]
            # Return the building data as JSON
            return JsonResponse({'name': name, 'lat': center["lat"], 'lon': center["lon"],'coord_list': coord_list})
        except:
            # Return a JSON response with the error message 'No results found'
            return JsonResponse({'error': 'No results found'}, status=404)
    else:
        # Return a 400 Bad Request error if the way ID is missing
        return JsonResponse({'error': 'Way ID is missing'}, status=400)

"""# function to extract data from the dataframe and pass that data to the database
def getRaveData(csvFile):
    # Only read the specific data that is relavent to the project
    columns = [" Site UID", " Answer", " Answer Received", " Answer LAT", " Answer LONG"]

    # Read the CSV file into a Pandas DataFrame
    resultsDataFrame = pd.read_csv(csvFile, usecols=columns)

    # Remove the last row from the Rave Data which contains "example@example" for several fields
    resultsDataFrame = resultsDataFrame[:-1]

    # Change the date time format from the data to match the date time format in the database
    resultsDataFrame[" Answer Received"] = pd.to_datetime(resultsDataFrame[" Answer Received"], format= "%b %d, %Y - %I:%M:%S %p")

    # create a map of the different column titles so that the data can be read from the dataframe to the database
    colMap = {" Site UID" : "id", " Answer" : "status", " Answer Received" : "created_at", " Answer LAT" : "lat", " Answer LONG" : "long"}

    # Send the information to the database
    for i, rowResult in resultsDataFrame.iterrows():
        # create an object of the poll data model
        pollRes = EmergencyModePollResult()
        
        # set the attributes for the poll result model to the values from the .csv file
        for colResult, value in rowResult.iteritems():
            setattr(pollRes, colMap[colResult], value)
        
        #save the object to the database
        pollRes.save()
"""
def getRaveData(csvFile):
    decoded_file = csvFile.read().decode('utf-8').splitlines()
    csv_reader = csv.DictReader(decoded_file)
    for row in csv_reader:
        # Skip rows where the ID is example@example.com
        if row[' Site UID'] == 'example@example.com':
            continue
            
        # Convert latitude and longitude to float or None
        lat = float(row[' Answer LAT']) if row[' Answer LAT'] else None
        long = float(row[' Answer LONG']) if row[' Answer LONG'] else None
        
        # Create a datetime object from the Answer Received field
        answer_received = datetime.strptime(row[' Answer Received'], "%b %d, %Y - %I:%M:%S %p")
        
        # Create an EmergencyModePollResult object and save it to the database
        obj = EmergencyModePollResult(
            id=row[' Site UID'],
            status=row[' Answer'],
            lat=lat,
            long=long,
            created_at=answer_received,
        )
        obj.save()

class BuildingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        building = self.get_object()
        serializer = self.get_serializer(building, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class EmergencyPollResultViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows poll requests to be viewed or edited.
    """
    queryset = EmergencyModePollResult.objects.all()
    serializer_class = EmergencyModePollResultSerializer
    permission_classes = [permissions.AllowAny]


class EmergencyModeIndicatorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows emergency mode indicators to be viewed or edited
    """
    queryset = EmergencyModeIndicator.objects.all()
    serializer_class = EmergencyModeIndicatorSerializer
    permission_classes = [permissions.AllowAny]


class DeviceCountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows emergency mode indicators to be viewed or edited
    """
    queryset = DeviceCount.objects.all()
    serializer_class = DeviceCountSerializer
    permission_classes = [permissions.AllowAny]