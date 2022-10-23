# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22

@author: Ryan Emadi
"""
import itertools
import requests
import math
import time

# Define Geocode API parameters
base_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
with open('API_KEY.txt', 'r') as keyFile:
	API_KEY = keyFile.readline()
keyFile.close()

# Get source address from user
source = input('Enter source address:\n')

# Get number of destinations
num_dests = input('Enter number of destinations: ')
# Error Check: Number of destinations needs to be between 1-4
try:
	num_dests = int(num_dests)
	if ((num_dests < 1) or (num_dests > 4)):
		raise Exception()
except:
	raise Exception('ERROR: Number of destinations needs to be between 1-4.')

# Get destination addresses from user
dests = [None]*num_dests
for i in range(num_dests):
	dests[i] = input('Enter destination address:\n')

# Start timer
start_time = time.time()
print('Starting program runtime.')

# Create permutations of all possible routes
dest_perms = itertools.permutations(dests)

# Cycle through all possible routes
all_perms = list()
total_times = list()
for perm in list(dest_perms):
	all_perms.append(perm)
	route_times = list()
	
	# 1) Get distance from source to first point
	req_url = f'{base_url} origins={source} &destinations={perm[0]} '\
		f'&mode=DRIVING &key={API_KEY}'
	req_url = req_url.replace(' ', '')
	req = requests.get(req_url).json()
	if req['status'] == 'OK':
		route_times.append(req['rows'][0]['elements'][0]['duration']['value'])
	else:
		raise Exception('ERROR: Invalid Address Input')
	
	# 2) Get distances from point to point
	for i in range(num_dests-1):
		this_req_url = f'{base_url} origins={perm[i]} '\
			f'&destinations={perm[i+1]} &mode=DRIVING &key={API_KEY}'
		this_req_url = this_req_url.replace(' ', '')
		this_req = requests.get(this_req_url).json()
		if req['status'] == 'OK':
			route_times.append(this_req['rows'][0]['elements'][0]\
				['duration']['value'])
		else:
			raise Exception('ERROR: Invalid Address Input')
	
	# 3) Add total time to list
	total_times.append(sum(route_times))

# Find fastest travel time
min_time = min(total_times)
min_index = total_times.index(min_time)
fastest_route = all_perms[min_index]

# Convert to hrs, mins
time_filt = math.ceil(min_time / 60)
time_hrs = math.floor(time_filt / 60)
time_mins = time_filt % 60

# Print fastest route to console
fastest_route_str = 'The optimal route is:\n'
for i in range(num_dests):
	fastest_route_str += f'{i+1}. {fastest_route[i]}\n'
fastest_route_str += f'which will take {time_hrs} hr, {time_mins} min.'
print(fastest_route_str)

# End timer
end_time = time.time()
elapsed_time = round(end_time-start_time, 6)
print(f'Program Runtime: {elapsed_time} sec')