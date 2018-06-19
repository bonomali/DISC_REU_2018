#!/usr/bin/python
"""The purpose of this script is to identify common substrings between strings of click data for different users
	e.g. if one user typically experiences-experiences-interacts and does that often, record that sequence, and list it as a substring"""

from collections import Counter
import datetime as dt
import csv
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from difflib import get_close_matches
from difflib import SequenceMatcher

csv_filepath = "SP18_all_data.csv"

#  First, load up the processed data (stored in a csv) as a list of dictionaries
with open(csv_filepath) as f:
	processed_data = [{k: str(v) for k, v in row.items()}
	for row in csv.DictReader(f, skipinitialspace=True)]

#~~~~~Now, replace the long "object_id" url strings with an id number~~~
objects = []
#  first create a list with every object id
for dictionary in processed_data:
	object_id = dictionary["object_id"]
	if "Coursework" in object_id:
		object_id = "Coursework"
	objects.append(object_id)

#  identify only unique object ids
object_types = list(set(objects))

#  make a dictionary with key:value pairs of object_id : ref_number
object_ref = {}
for index in range(len(object_types)):
	object_ref[object_types[index]] = str(index)





#################################################
#  Generate a string of 0 (interacted) and 1 (experienced), to look for patterns in behaviour.
#################################################
def activity_string_generator(data_dict, name):
	sorted_dicts = sorted(data_dict, key=lambda k: k["timestamp"])
	activity_string = name + " "
	
	start_time = dt.datetime.strptime(sorted_dicts[0]["timestamp"], '%Y-%m-%dT%H:%M:%S')
	for entry in sorted_dicts:
		# get current time
		time_now = dt.datetime.strptime(entry["timestamp"], '%Y-%m-%dT%H:%M:%S')
		# get total time (in seconds) between last entry and this entry
		delta_t = (time_now - start_time).total_seconds()	
		# if time taken is between 15 minutes and 3 hours
		# add 30 minute blocks of short idle time
		if delta_t >= 900. and delta_t <10800.:
			while delta_t >900:
				delta_t += -1800
				activity_string += str(len(object_ref)+1) + " "
		# if time taken is greater than 3 hours, add one long idle time
		elif delta_t >=10800.:
			activity_string += str(len(object_ref)+2) + " "
		
		# regardless of how much idle time has been added
		# the ref_id of the activity must be added too
		object_id =entry["object_id"]
		if "Coursework" in object_id:
			object_id = "Coursework"
		activity_string += object_ref[object_id] + " "
		start_time = time_now
	return activity_string

#################################################
#Find indices corresponding to a key:value pair in a list of dictionaries
#################################################
def find(lst, key, value):
	indices = []
	for i, dic in enumerate(lst):
		if dic[key] == value:
			indices.append(i)
	return indices

#For now, just pull out the names of the ~100 people that make the most clicks, to have a large sample size
entries_by_name = Counter(x['account_name'] for x in processed_data)
names = entries_by_name.keys()
values = entries_by_name.values()
names = [x for _,x in sorted(zip(values, names), reverse=True)][:500]

#Generate a list of activity strings, one for each name
all_data = []
for name in names:
	indices = find(processed_data, "account_name", name)
	cut_data = processed_data[indices[0]:indices[-1]+1]
	new_data = activity_string_generator(cut_data, name)##, color = color)
	all_data.append(new_data)


outputfile = open('sequence.txt', 'w')
for item in all_data:
  outputfile.write("%s\n" % item)

#  To convert each activity string to a list of elements instead:

with open('object_ref.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in object_ref.items():
       writer.writerow([key, value])

#match = SequenceMatcher(None, string1, string2).get_matching_blocks()

#################################################
#Let's develop our own string matching mechanism.
#################################################

"""match_list = []
for i in range(len(all_data)):
	for j in range(len(all_data)):
		if i != j:
			matches = SequenceMatcher(None, all_data[j], all_data[i]).get_matching_blocks()
			for ind in range(len(matches) -1 ):
				match = all_data[j][matches[ind].a : matches[ind].a + matches[ind].size] 
				
				match_list.append(match)

#count the unique items for comparison purposes




for key, value in object_ref.iteritems():
    if value == '18':
        print(key)"""
