#!/usr/bin/python
"""The purpose of this script is to produce one large textfile containing sequence data for each student, one sequence per line.
	Furthermore, it will also produce "sub"-text files containing sequence data for each student PER WEEK, i.e. one new file per week."""

from collections import Counter
import datetime as dt
import csv
import sys
import numpy as np

#  Function to get dictionary key from value (i.e. opposite of usual)
def find(lst, key, value):
	indices = []
	for i, dic in enumerate(lst):
		if dic[key] == value:
			indices.append(i)
	return indices


num_students = 200

"""
####################################################################################################
LOAD UP AND FURTHER PROCESS ALL CSV FILES
####################################################################################################
"""

click_filepath = "SP18_all_data.csv"
activity_filepath = "activity_type.csv"
submission_filepath = "SP18_assignments_activty.csv"

###  First, load up the processed click data (stored in a csv) as a list of dictionaries
with open(click_filepath) as f:
	click_data = [{k: str(v) for k, v in row.items()}
	for row in csv.DictReader(f, skipinitialspace=True)]

###  Then, load up the activity_type (reading, coursework, or video) data (also stored in a csv) as a list of dictionaries
with open(activity_filepath) as fp:
	activity_type = [{k: str(v) for k, v in row.items()}
	for row in csv.DictReader(fp, skipinitialspace=True)]

###  Now, replace the long "object_id" url strings with an id number, activity_type and week
objects = []
###  first create a list with every object id
for dictionary in click_data:
	object_id = dictionary["object_id"]
	if "Coursework" in object_id:
		object_id = "Coursework"
	objects.append(object_id)

###  identify only unique object ids
object_types = list(set(objects))

###  make a dictionary with key:value pairs of object_id : {ref_num: number, activity_type: type, week: week}
object_ref = {}
for index in range(len(object_types)):
	object_id = object_types[index]
	ref_num = str(index)
	###  pull the corresponding url dict from activity_type to get out the other needed info
	activity_dict = next((item for item in activity_type if item['url'] == object_id))
	activity = activity_dict["type"]
	week = activity_dict["week"]
	
	object_ref[object_id] = {"ref_num":ref_num, "activity_type": activity, "week":week}

###  Only use the first 500 names cos otherwise we get some low-sequence info that isn't very useful
entries_by_name = Counter(x['account_name'] for x in click_data)
names = entries_by_name.keys()
values = entries_by_name.values()
names = [x for _,x in sorted(zip(values, names), reverse=True)][:num_students]


###  Now, load up the assignment submission data (stored in a csv) as another list of dictionaries
with open(submission_filepath) as f:
	submission_data = [{k: str(v) for k, v in row.items()}
	for row in csv.DictReader(f, skipinitialspace=True)]

###  Sort submission data by user
submissions_by_name = {}
for name in names:
	submissions = []
	for submission in submission_data:
		if submission["account_name"] == name:
			entry = {"timestamp":submission["timestamp"], "assignment":submission["object_id"]}
			submissions.append(entry)
	submissions_by_name[name] = submissions

###  Now, remove duplicate entries, i.e. only keep the latest submission for an assignment.
sorted_submissions_by_name = {}
for name in list(submissions_by_name.keys()):
	submissions_ordered = sorted(submissions_by_name[name], key=lambda k: k['timestamp']) 
	try:
		assignment = submissions_ordered[0]["assignment"]
		submissions_no_duplicates = []		
		for index in range(1,len(submissions_ordered)):
			next_assignment = submissions_ordered[index]["assignment"]
			if next_assignment != assignment:
				submissions_no_duplicates.append(submissions_ordered[index])
			assignment = next_assignment
		sorted_submissions_by_name[name] = submissions_no_duplicates
	except:
		## This except statement arises when a student has 0 submissions
		sorted_submissions_by_name[name] = [{"assignment": None, "object_id" : None, "timestamp": None}]





"""
###############################################################################################
#  Generate a string of object-number sequences.
#  If split = True, breaks up the sequence at long idle times.
###############################################################################################
"""

def activity_string_generator_ALL(data_dict, name, split = False):
	sorted_dicts = sorted(data_dict, key=lambda k: k["timestamp"])
	activity_string = name + " "
	if split == True:
		split_count = 0
	start_time = dt.datetime.strptime(sorted_dicts[0]["timestamp"], '%Y-%m-%dT%H:%M:%S')
	for entry in sorted_dicts:
		# get current time
		time_now = dt.datetime.strptime(entry["timestamp"], '%Y-%m-%dT%H:%M:%S')
		# get total time (in seconds) between last entry and this entry
		delta_t = (time_now - start_time).total_seconds()	
		# if time taken is between 30 minutes and 3 hours
		# add 30 minute blocks of short idle time
		if delta_t >= 1800. and delta_t <10800.:
			while delta_t >900:
				delta_t += -1800
				activity_string += str(len(object_ref)+1) + " "
		# if time taken is greater than 3 hours, add one long idle time
		elif delta_t >=10800.:
			activity_string += str(len(object_ref)+2) + " "
			if split == True:
				activity_string += "\n"
				activity_string += name + str(split_count) + " "	
				split_count +=1		
		# regardless of how much idle time has been added
		# the ref_id of the activity must be added too
		object_id = entry["object_id"]
		if "Coursework" in object_id:
			object_id = "Coursework"
		activity_string += object_ref[object_id]["ref_num"] + " "
		
		start_time = time_now
	
	return activity_string


def activity_string_generator_byassignment(data_dict, submissions_list, name):
	sorted_dicts = sorted(data_dict, key=lambda k: k["timestamp"])
	submission_counter = 0
	object_id = sorted_dicts[0] ["object_id"]
	if "Coursework" in object_id:
		object_id = "Coursework"
	start_click = object_ref[ object_id ]["ref_num"]
	
	if submissions_list[0]["timestamp"] == None:
		strings_dict = {}
		submission_time = dt.datetime.max
		start_time = dt.datetime.strptime(sorted_dicts[0]["timestamp"], '%Y-%m-%dT%H:%M:%S')
		assignment = "None"
		strings_dict[assignment + "_clicks"] = name +  " " 
		strings_dict[assignment + "_times"] = name + " "
	else:
		strings_dict = {}
		submission_time = dt.datetime.strptime(submissions_list[0]["timestamp"], '%Y-%m-%dT%H:%M:%S')
		start_time = dt.datetime.strptime(sorted_dicts[0]["timestamp"], '%Y-%m-%dT%H:%M:%S')	
		assignment = submissions_list[submission_counter]["assignment"]
		strings_dict[assignment + "_clicks"] = name +  " " 
		strings_dict[assignment + "_times"] = name + ","
	
	for entry in sorted_dicts:
		##  get current time
		time_now = dt.datetime.strptime(entry["timestamp"], '%Y-%m-%dT%H:%M:%S')
		delta_t = (time_now - start_time).total_seconds()	
		
		##  change submission time when assignment changes
		if time_now >= submission_time:
			#  Append the completed string of activities that took place this week to the full weeks list
			if submission_counter < len(submissions_list)-1:
				strings_dict[assignment + "_clicks"] += "100"	
				strings_dict[assignment + "_times"] += str(submission_time)
				submission_counter += 1
				assignment = submissions_list[submission_counter]["assignment"]
				strings_dict[assignment + "_clicks"] = name + " "	
				strings_dict[assignment + "_times"] = name + ","
				submission_time = dt.datetime.strptime(submissions_list[submission_counter]["timestamp"], '%Y-%m-%dT%H:%M:%S')
				
			else:
				assignment = "Revision"
				strings_dict[assignment + "_clicks"] = name + " "
				strings_dict[assignment + "_times"] = name + ","
				submission_time = dt.datetime.max 
		
		## regardless of how much idle time has been added, the ref_id of the activity must be added too
		object_id = entry["object_id"]
		if "Coursework" in object_id:
			object_id = "Coursework"
		
		click_now = object_ref[object_id]["ref_num"]
		
		strings_dict[assignment + "_clicks"] += click_now + " "
		strings_dict[assignment + "_times"] += str(time_now) + ","
		if not (click_now == start_click and object_id == "Coursework"):
			
			## Otherwise, provided this week isn't different, you want to take account for possible idle time.
			if delta_t >= 15*60. and delta_t <30*60.:
				strings_dict[assignment + "_clicks"] += str(len(object_ref)+1) + " "
				strings_dict[assignment + "_times"] += str(time_now - datetime.timedelta(minutes=15)) + " "
			## if time taken is greater than 3 hours, add one long idle time
			elif delta_t >= 30*60. and delta_t <45*60.:
				strings_dict[assignment + "_clicks"] += str(len(object_ref)+1) + " "
				strings_dict[assignment + "_times"] += str(time_now - datetime.timedelta(minutes=30)) + " "
			elif delta_t >= 45*60. and delta_t <60*60.:
				strings_dict[assignment + "_clicks"] += str(len(object_ref)+1) + " "
				strings_dict[assignment + "_times"] += str(time_now - datetime.timedelta(minutes=45)) + " "
			elif delta_t >= 60*60.:
				strings_dict[assignment + "_clicks"] += str(len(object_ref)+1) + " "
				strings_dict[assignment + "_times"] += str(time_now - datetime.timedelta(minutes=60)) + " "
		
			strings_dict[assignment + "_clicks"] += click_now + " "
			strings_dict[assignment + "_times"] += str(time_now) + " "
		
		start_click = click_now
		start_time = time_now
		
	return strings_dict

"""
###############################################################################################################
##                         Call functions to generate output txt sequences
###############################################################################################################
"""

#  Generate a list of dictionaries of activity strings, one for each name for each week
all_data_byassignment = []
for name in names:
	print(name)
	indices = find(click_data, "account_name", name)
	cut_data = click_data[indices[0]:indices[-1]+1]
	submissions_list = sorted_submissions_by_name[name]
	new_data = activity_string_generator_byassignment(cut_data, submissions_list, name)##, color = color)
	all_data_byassignment.append(new_data)


#  Collect up keys for each person and find out which weeks you need to check for.
keys = []
for dictionary in all_data_byassignment:
	for key in list(dictionary.keys()):
		keys.append(key)

keys = list(set(keys))

for key in keys:
	list_byweek = []
	for dictionary in all_data_byassignment:
		if key in dictionary:
			list_byweek.append(dictionary[key])
	outfile_byweek = open('sequence' + key + '.txt', 'w')
	for item in list_byweek:
		outfile_byweek.write("%s\n" % item)

"""
#  Generate the master list of all activity strings, one for each name (covering the entire duration
all_data = []
for name in names:
	indices = find(click_data, "account_name", name)
	cut_data = click_data[indices[0]:indices[-1]+1]
	new_data = activity_string_generator_ALL(cut_data, name)##, color = color)
	all_data.append(new_data)

outputfile = open('sequence.txt', 'w')
for item in all_data:
  outputfile.write("%s\n" % item)

#  To convert each activity string to a list of elements instead:

with open('object_ref.csv', 'w') as csv_file:
	writer = csv.writer(csv_file)
	for key, value in object_ref.items():
		writer.writerow([key, value])

"""
