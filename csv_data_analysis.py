#!/usr/bin/python
"""This script takes our processed files and works some magic on them to get useful info.
	Right now, I don't know what the useful info is, or what the magic that can be worked is...
	but i'm sure I'll figure it out eventually."""

from collections import Counter
import datetime as dt
import csv
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

csv_filepath = "SP18_all_data.csv"

#################################################
#First, load up the processed data (stored in a csv) as a list of dictionaries
#################################################
with open(csv_filepath) as f:
	processed_data = [{k: str(v) for k, v in row.items()}
	for row in csv.DictReader(f, skipinitialspace=True)]


#################################################
#Maybe see how -all- entries vary over time?
#################################################
def plot_activity_by_date(data_dict, name = "N/A", total_days = 133):
	experiences_by_date = Counter(x["date"] for x in data_dict if x["verb_id"] == "experienced")
	interactions_by_date = Counter(x["date"] for x in data_dict if x["verb_id"]=="interacted")
	colors = ['red', 'green', 'green', 'blue', 'black', 'black']
	labels = ['Experienced', 'Interacted']
	colindex = 0
	
	for entries_by_date in [experiences_by_date, interactions_by_date]:
		dates_strings = entries_by_date.keys()
		values = entries_by_date.values()
		datetimes = [dt.datetime.strptime(str(date), '%Y-%m-%d').date() for date in dates_strings]
		
		values_sorted = [x for _,x in sorted(zip(datetimes, values))]
		#values_sorted[:] = [x / divisor for x in values_sorted]
		dates_sorted = sorted(datetimes)
		
		np_dates = np.array(dates_sorted)
		np_values = np.array(values)
		
		#~~~~~~~~If you want to include every single day, even those with zero clicks~~~~~~~~~
		base = dt.date(2018, 1, 2)
		all_dates = np.array([base + dt.timedelta(days=i) for i in xrange(total_days)])
		
		missing_dates = np.pad(np_dates, (0,total_days), 'constant', constant_values = (0, 0))
		missing_values = np_values
		
		for i in range(133):
			if all_dates[i] != missing_dates[i]:
				missing_dates = np.insert(missing_dates, i, all_dates[i])
				missing_values = np.insert(missing_values, i, 0)
		missing_dates = missing_dates[:-total_days]
		
		np_dates = missing_dates
		np_values = missing_values
		
		mean_val = np.mean(np_values)
		median_val = np.median(np_values)
		
		np_all_data = {"dates_array": np_dates, "values_array": np_values, "name": name}
		
		if median_val < 0.6 * mean_val:
			np_all_data["Type"] = "Cluster"
		
		elif median_val > 0.7 * mean_val:
			np_all_data["Type"] = "Consistent"
		
		else:
			np_all_data["Type"] = "Clustered consistent"
		
		#dates = mdates.date2num(dates_sorted)
		plt.plot(np_dates, np_values, color = colors[colindex], label = labels[colindex], ls = '-', marker = 'o')
		plt.plot( np_dates, np.full(len(np_dates), mean_val),  color = colors[colindex*2], ls = '--')
		plt.plot( np_dates, np.full(len(np_dates), median_val), color = colors[colindex*3], ls = ':')
		plt.grid(True)
		plt.title(np_all_data["Type"])
		plt.legend(loc = 'best')
		
		colindex +=1
	return np_all_data


#################################################
#ALternatively, instead of going by clicks per day, look at clicks per week instead.#
#################################################
def plot_activity_by_week(data_dict, name = "N/A", total_days = 133):
	entries_by_week = Counter(x["week"] for x in data_dict)
	weeks_unsorted = map(int, entries_by_week.keys())
	values_unsorted = entries_by_week.values()
	
	values_sorted = [x for _,x in sorted(zip(weeks_unsorted, values_unsorted))]
	values_sorted[:] = [x / divisor for x in values_sorted]
	weeks_sorted = sorted(weeks_unsorted)
	
	weeks = np.array(weeks_sorted)
	values = np.array(values_sorted)
	
	#~~~~~~~~If you want to include every single week, even those with zero clicks~~~~~~~
	all_weeks = np.arange(2,21,1)
	
	#Pad the righthandside of the weeks array with zeros so you don't get index errors
	missing_weeks = np.pad(weeks, (0,21), 'constant', constant_values = (0, 0))
	missing_values = values
	
	#Insert missing weeks with a value of 0
	for i in range(len(all_weeks)):
		if all_weeks[i] != missing_weeks[i]:
			missing_weeks = np.insert(missing_weeks, i, all_weeks[i])
			missing_values = np.insert(missing_values, i, 0)
	#now cut out the padded zeros:
	missing_weeks = missing_weeks[:-21]
	
	weeks = missing_weeks
	values = missing_values
	
	mean_val = np.mean(values)
	median_val = np.median(values)
	
	np_all_data = {"dates_array": weeks, "values_array": values, "name": name}
	
	if median_val < 0.6 * mean_val:
		np_all_data["Type"] = "Cluster"
	
	elif median_val > 0.7 * mean_val:
		np_all_data["Type"] = "Consistent"
	
	else:
		np_all_data["Type"] = "Clustered consistent"
	
	plt.plot(weeks, values, color = color, ls = '-', marker = 'o')
	plt.plot( weeks, np.full(len(weeks), mean_val), ls = '--')
	plt.plot( weeks, np.full(len(weeks), median_val), ls = ':')
	plt.title(np_all_data["Type"])	
	return np_all_data

#################################################
#Find indices corresponding to a key:value pair in a list of dictionaries
#################################################
def find(lst, key, value):
	indices = []
	for i, dic in enumerate(lst):
		if dic[key] == value:
			indices.append(i)
	return indices

#################################################
#Plot a bunch of clicks:week / clicks:date graphs to look for trends visually
#################################################

chopped_data = processed_data
#For now, just pull out the most-clicked 25 people

entries_by_name = Counter(x['account_name'] for x in chopped_data)
names = entries_by_name.keys()
values = entries_by_name.values()
names = [x for _,x in sorted(zip(values, names), reverse=True)][:10]

all_data = []
for name in names:
	plt.figure()
	indices = find(chopped_data, "account_name", name)
	cut_data = chopped_data[indices[0]:indices[-1]+1]
	#color = plt.cm.hsv((1.0/ len(names)*col_counter))
	
	new_data = plot_activity_by_date(cut_data, name = name)##, color = color)
	all_data.append(new_data)
