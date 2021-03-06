#!/usr/bin/python
"""This script processes our JSON files, cutting out unnecessary information and flattening data to return a csv.
	The defined function can be used either by:
		- import into a different programme, or
		- from the command line, giving json_filepath and csv_filepath as command line arguments.
	In both cases, the INPUTS:
		- json_filepath should be the location of the raw (JSON format) data, and  
		- csv_filepath should be the desired location of the processed (CSV format) data"""

import csv
import json
import sys
import datetime as dt


#json_filepath = "SP18RawActivityData/SP18_FYS_10101_activity_03_23.json"
#csv_filepath = "SP18_03_23.csv"
json_filepath = "SP18RawActivityData/SP18_FYS_10101_assignments_activity_submission_05_14.json"
csv_filepath = "SP18CSVData/SP18_assignments_activty.csv"

def raw_data_to_csv(json_filepath, csv_filepath, activity_type = False):
	f = open(json_filepath, 'r')
	json_value = f.read()
	raw_data = json.loads(json_value)
	f.close()
	
	#The only data we care about is stored in the subkey "hits" of the main key "hits"
	#relevant_data is then a list of dictionaries, where each dictionary corresponds to a single action
	relevant_data = raw_data["hits"]["hits"]
	
	processed_data = []
	for d in relevant_data:
		#pick out wanted info
		account_name = d["_source"]["actor"]["account"]["name"]
		date = d["_source"]["timestamp"][:10]
		time = d["_source"]["timestamp"][11:-6]
		week = int((dt.datetime.strptime(str(date), '%Y-%m-%d').date()).strftime("%W"))
		timestamp = d["_source"]["timestamp"][:-6]
		object_id = d["_source"]["object"]["id"]
		if activity_type == True:
			description = d["_source"]["object"]["definition"]["description"]["en-US"]
			
			if "ePortfolio Access and Link Check" in description:
				object_id= "ePortfolio Link"
			
			elif "Capstone ePortfolio" in description:
				object_id = "Capstone"
			
			elif "Integration #3" in description:
				object_id = "Integration3"
			
			else:
				for check in ["#11", "#10", "#9", "#8", "#7", "#6", "#5", "#4", "#3", "#2", "#1"]:
					if check in description:
						object_id = "Prompt" + check[1:]
						break
			
		#for verb_id info, we don't want to include the dumb url before it, so keep only the end characters
		verb_id = d["_source"]["verb"]["id"][35:] 
		
		#make a new dictionary with wanted info
		d_entry = {"account_name": account_name, "date": date, "time" :time, "timestamp":timestamp, "week": week, "object_id":object_id, "verb_id": verb_id}
		
		#append to the output info
		processed_data.append(d_entry)
	
	processed_data_sorted = sorted(processed_data, key=lambda k: k["account_name"])
	
	keys = processed_data_sorted[0].keys()
	with open(csv_filepath, 'w') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(processed_data_sorted)

if len(sys.argv) != 1:
	if "activity" in sys.argv[1]:
		raw_data_to_csv(sys.argv[1], sys.argv[2], activity_type = True)
	else:
		raw_data_to_csv(sys.argv[1], sys.argv[2])
