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

#First, load up the processed data (stored in a csv) as a list of dictionaries
with open(csv_filepath) as f:
	processed_data = [{k: str(v) for k, v in row.items()}
	for row in csv.DictReader(f, skipinitialspace=True)]



##Maybe see how -all- entries vary over time?
def plot_activity_by_date(data_dict, name = "N/A", color = 'black', divisor = 1, total_days = 133):
	entries_by_date = Counter(x["date"] for x in data_dict)
	
	dates_strings = entries_by_date.keys()
	values = entries_by_date.values()
	datetimes = [dt.datetime.strptime(str(date), '%Y-%m-%d').date() for date in dates_strings]
	
	values_sorted = [x for _,x in sorted(zip(datetimes, values))]
	values_sorted[:] = [x / divisor for x in values_sorted]
	dates_sorted = sorted(datetimes)
	
	np_dates = np.array(dates_sorted)
	np_values = np.array(values)
	
	'''#If you want to include every single day, even those with zero clicks, use the following:
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
	median_val = np.median(np_values)'''
	
	np_all_data = {"dates_array": np_dates, "values_array": np_values, "name": name}
	
	if median_val < 0.6 * mean_val:
		np_all_data["Type"] = "Cluster"
	
	elif median_val > 0.7 * mean_val:
		np_all_data["Type"] = "Consistent"
	
	else:
		np_all_data["Type"] = "Clustered consistent"
	
	#dates = mdates.date2num(dates_sorted)
	plt.plot(np_dates, np_values, color = color)#, ls = '-', marker = 'o')
	plt.plot( np_dates, np.full(len(np_dates), mean_val), ls = '--')
	plt.plot( np_dates, np.full(len(np_dates), median_val), ls = ':')
	plt.title(np_all_data["Type"])
	
	return np_all_data


##how about individual entries? overplot on the -all- entries one...
def find(lst, key, value):
	indices = []
	for i, dic in enumerate(lst):
		if dic[key] == value:
			indices.append(i)
	return indices


chopped_data = processed_data[:5000]
entries_by_name = Counter(x['account_name'] for x in chopped_data)
names = entries_by_name.keys()
col_counter = 0

all_data = []
for name in names:
	plt.figure()
	indices = find(chopped_data, "account_name", name)
	cut_data = chopped_data[indices[0]:indices[-1]+1]
	color = plt.cm.hsv((1.0/ len(names)*col_counter))
	
	new_data = plot_activity_by_date(cut_data, name = name, color = color)
	list_of_all_data.append(new_data)
	
	col_counter += 1






'''divisor = float(len(Counter(x["account_name"] for x in chopped_data)))
print(divisor)
plot_activity_by_date(chopped_data, color = "black", divisor = divisor)
'''
