import datetime as dt
import numpy as np
import csv 
import matplotlib.pyplot as plt

testfile = "sequencePrompt9_times_test.txt"

clicks = []
with open(testfile) as f:
	for line in csv.reader(f, delimiter = ","):
		clicks.append(line[1:])

timedeltas = []
for line in clicks:
	for index in range(len(line)-1):
		click_now = dt.datetime.strptime(line[index], '%Y-%m-%d %H:%M:%S')	
		next_click = dt.datetime.strptime(line[index+1], '%Y-%m-%d %H:%M:%S')	
		delta_t = next_click - click_now
		delta_t = dt.timedelta.total_seconds(delta_t)/60
		timedeltas.append(delta_t)

bins = np.arange(0, 60*4, 15)
n, bins, patches = plt.hist(timedeltas, bins=bins, color='green')
