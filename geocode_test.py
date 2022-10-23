# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22

@author: remadi
"""
import requests

# Define Geocode API parameters
base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
API_KEY = 'AIzaSyDmG68AvFsmx1Rpge2cUI_7F_JvDlX-EAg'

# Define address
address = '777 Atlantic Dr NW, Atlanta, GA 30313'

# Set up parameter dict
params = {
	'key': API_KEY,
	'address': address
}

# Get response
response = requests.get(base_url, params=params).json()

# Extract latitude and longitude from response
if response['status'] == 'OK':
	geometry = response['results'][0]['geometry']
	latitude = round(geometry['location']['lat'], 5)
	longitude = round(geometry['location']['lng'], 5)

print(f'Latitude: {latitude}\nLongitude: {longitude}')