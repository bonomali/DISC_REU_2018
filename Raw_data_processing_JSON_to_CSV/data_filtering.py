#!/usr/bin/python
"""The purpose of this script is to produce one large textfile containing sequence data for each student, one sequence per line.
	Furthermore, it will also produce "sub"-text files containing sequence data for each student PER WEEK, i.e. one new file per week."""

from collections import Counter
import datetime as dt
import csv
import sys
import numpy as np

import json_conversion_to_csv as json_converter
import csv_joiner

#  Function to get dictionary key from value (i.e. opposite of usual)
def find(lst, key, value):
	indices = []
	for i, dic in enumerate(lst):
		if dic[key] == value:
			indices.append(i)
	return indices



"""
####################################################################################################
              CONVERT JSON FILES TO CSV, TIE CSV FILES TOGETHER, AND PROCESS FILES
####################################################################################################
"""


click_filepath = "SP18CSVData/SP18_all_data.csv"
activity_filepath = "SP18CSVData/activity_type.csv"
submission_filepath = "SP18CSVData/SP18_assignments_activity.csv"

##  First, load up the processed click data and activity type (stored in a csv) as a list of dictionaries
with open(click_filepath) as f:
	click_data = [{k: str(v) for k, v in row.items()}
	for row in csv.DictReader(f, skipinitialspace=True)]

with open(activity_filepath) as fp:
	activity_type = [{k: str(v) for k, v in row.items()}
	for row in csv.DictReader(fp, skipinitialspace=True)]

##  Now, generate object_ref file
objects = []
for dictionary in click_data:
	object_id = dictionary["object_id"]
	if "Coursework" in object_id:
		object_id = "Coursework"
	objects.append(object_id)

object_types = list(set(objects))
object_ref = {}
for index in range(len(object_types)):
	object_id = object_types[index]
	ref_num = str(index)
	###  pull the corresponding url dict from activity_type to get out the other needed info
	activity_dict = next((item for item in activity_type if item['url'] == object_id))
	activity = activity_dict["type"]
	week = activity_dict["week"]
	object_ref[object_id] = {"ref_num":ref_num, "activity_type": activity, "week":week}


###  Only use the first 500-most-clicks-names
num_students = 1000
entries_by_name = Counter(x['account_name'] for x in click_data)
names = [x for _,x in sorted(zip(entries_by_name.values(), entries_by_name.keys()), reverse=True)][:num_students]


##  Load up the submission data as another list of dictionaries
##  and sort by user
with open(submission_filepath) as f:
	submission_data = [{k: str(v) for k, v in row.items()}
	for row in csv.DictReader(f, skipinitialspace=True)]

submissions_by_name = {}
for name in names:
	submissions = []
	for submission in submission_data:
		if submission["account_name"] == name:
			entry = {"timestamp":submission["timestamp"], "assignment":submission["object_id"]}
			submissions.append(entry)
	submissions_by_name[name] = submissions

###  Remove duplicate entries, i.e. only keep the latest submission for an assignment.
def sorted_submissions_by_name(name):
	submissions_ordered = sorted(submissions_by_name[name], key=lambda k: k['timestamp']) 
	try:
		assignment = submissions_ordered[0]["assignment"]
		submissions_no_duplicates = []
		if len(submissions_ordered) > 1:	
			for index in range(1,len(submissions_ordered)):
				next_assignment = submissions_ordered[index]["assignment"]
				if next_assignment != assignment:
					submissions_no_duplicates.append(submissions_ordered[index])
				assignment = next_assignment
			sorted_submissions = submissions_no_duplicates
		else:
			sorted_submissions = submissions_ordered
	except:
		## This except statement arises when a student has 0 submissions
		sorted_submissions = [{"assignment": None, "object_id" : None, "timestamp": None}]
	return sorted_submissions


"""
###############################################################################################
                       Generate a string of object-number sequences.
               If split = True, breaks up the sequence at long idle times.
###############################################################################################
"""

def activity_string_generator_byassignment(data_dict, submissions_list, name, 
										   include_idle = True, separate_assignment = True):
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
		if separate_assignment == True:
			assignment = submissions_list[submission_counter]["assignment"]
		else:
			assignment = "All"
		strings_dict[assignment + "_clicks"] = name +  " " 
		strings_dict[assignment + "_times"] = name + ","
	
	for entry in sorted_dicts:
		time_now = dt.datetime.strptime(entry["timestamp"], '%Y-%m-%dT%H:%M:%S')
		delta_t = (time_now - start_time).total_seconds()
		##  change submission time + change assignment name when assignment changes
		if time_now >= submission_time:
			if submission_counter < len(submissions_list)-1:
				strings_dict[assignment + "_clicks"] += "100"
				strings_dict[assignment + "_times"] += str(submission_time)
				submission_counter += 1
				if separate_assignment == True:
					assignment = submissions_list[submission_counter]["assignment"]
					strings_dict[assignment + "_clicks"] = name + " "
					strings_dict[assignment + "_times"] = name + ","
				else:
					strings_dict[assignment + "_clicks"] 
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
		if not (click_now == start_click and object_id == "Coursework" and include_idle == True):
			
			## Account for idle time
			if delta_t >= 15*60. and delta_t <30*60.:
				strings_dict[assignment + "_clicks"] += str(len(object_ref)+1) + " "
				strings_dict[assignment + "_times"] += str(time_now - dt.timedelta(minutes=15)) + " "
			elif delta_t >= 30*60. and delta_t <45*60.:
				strings_dict[assignment + "_clicks"] += str(len(object_ref)+2) + " "
				strings_dict[assignment + "_times"] += str(time_now - dt.timedelta(minutes=30)) + " "
			elif delta_t >= 45*60. and delta_t <60*60.:
				strings_dict[assignment + "_clicks"] += str(len(object_ref)+3) + " "
				strings_dict[assignment + "_times"] += str(time_now - dt.timedelta(minutes=45)) + " "
			elif delta_t >= 60*60. and delta_t < 60*120:
				strings_dict[assignment + "_clicks"] += str(len(object_ref)+4) + " "
				strings_dict[assignment + "_times"] += str(time_now - dt.timedelta(minutes=60)) + " "
			elif delta_t >= 60*120.:
				strings_dict[assignment + "_clicks"] += str(len(object_ref)+5) + " "
				strings_dict[assignment + "_times"] += str(time_now - dt.timedelta(minutes=60)) + " "
		
			strings_dict[assignment + "_clicks"] += click_now + " "
			strings_dict[assignment + "_times"] += str(time_now) + " "
		
		start_click = click_now
		start_time = time_now
		
	return strings_dict

"""
###############################################################################################################
#                               Call functions to generate output txt sequences
###############################################################################################################
"""

#  Generate a list of dictionaries of activity strings, one for each name for each week
all_data_byassignment = []
for name in names:
	indices = find(click_data, "account_name", name)
	cut_data = click_data[indices[0]:indices[-1]+1]
	submissions_list = sorted_submissions_by_name(name)
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
	outfile_byweek = open("Sequence_Data/"+'sequence' + key + '.txt', 'w')
	print("Sequence_Data/"+'sequence')
	for item in list_byweek:
		outfile_byweek.write("%s\n" % item)
