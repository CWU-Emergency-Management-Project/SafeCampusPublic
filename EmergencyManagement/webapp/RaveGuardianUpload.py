import os
import sys
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import django
from django.conf import settings

# Connect to Django project
sys.path.append('I:\School\CS481\Emergency-Management\EmergencyManagement')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmergencyManagement.settings')
django.setup()

# import the database connection from django
from django.db import connection

# Get the django model that we will use to read into the databse
from webapp.models import EmergencyModePollResult, EmergencyModeIndicator

# function to get a .csv file from the user using pandas and read the contents of that file into a pandas dataframe object
def getFileandData():
	# Open Windows Explorer to select the CSV file
	root = tk.Tk()
	root.withdraw()
	file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])

	# Only read the specific data that is relavent to the project
	columns = [" Site UID", " Answer", " Answer Received", " Answer LAT", " Answer LONG"]

	# Read the CSV file into a Pandas DataFrame
	resultsDataFrame = pd.read_csv(file_path, usecols=columns)
	
	# Remove the last row from the Rave Data which contains "example@example" for several fields
	resultsDataFrame = resultsDataFrame[:-1]

	# Change the date time format from the data to match the date time format in the database
	resultsDataFrame[" Answer Received"] = pd.to_datetime(resultsDataFrame[" Answer Received"], format= "%b %d, %Y - %I:%M:%S %p")

	# Return the dataframe data read from the CSV file
	return resultsDataFrame

# function to extract data from the dataframe and pass that data to the database
def getRaveData():
	print("Data retrieval method")
	#call the function to get the datafram object with all of the .csv information
	results = getFileandData()
	
	# create a map of the different column titles so that the data can be read from the dataframe to the database
	colMap = {" Site UID" : "id", " Answer" : "status", " Answer Received" : "created_at", " Answer LAT" : "lat", " Answer LONG" : "long"}
	
	# Send the information to the database
	for i, rowResult in results.iterrows():
		# create an object of the poll data model
		pollRes = EmergencyModePollResult()
		
		# set the attributes for the poll result model to the values from the .csv file
		for colResult, value in rowResult.iteritems():
			setattr(pollRes, colMap[colResult], value)
		
		#save the object to the database
		pollRes.save()
		
	# close connection to database
	connection.close()

getRaveData()