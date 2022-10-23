# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22

@author: remadi
"""
import requests
import json
import math

# Define Geocode API parameters
base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
API_KEY = 'AIzaSyDmG68AvFsmx1Rpge2cUI_7F_JvDlX-EAg'

# Source address (Bobby Dodd Stadium)
source = '177 North Ave NW, Atlanta, GA 30313'

# Destination address (Sanford Stadium)
dest1 = '100 Sanford Dr, Athens, GA 30602'

# Construct request URL
req_url = f'{base_url} origins={source} &destinations={dest1} '\
	f'&mode=DRIVING &key={API_KEY}'
req_url = req_url.replace(' ', '')

# Get request
req = requests.get(req_url).json()

# Process request
if req['status'] == 'OK':
	# Extract destination time
	time = math.ceil(req['rows'][0]['elements'][0]['duration']['value'] / 60)
	hrs = math.floor(time / 60)
	mins = time % 60
	
	# Print destination time
	print(f'Trip will take {hrs} hr, {mins} min')
else:
	print('ERROR: Invalid Request!')