#!/usr/bin/python
"""This script processes takes our processed CSV files and adjoins them into one large CSV, to make data analysis easier.
	INPUTS:
		- filenames of each file to be adjoined
		- followed by the csv filename"""

import csv
import json
import sys

if len(sys.argv) != 1:
	filepaths = sys.argv[1:-1]
	csv_output = sys.argv[-1]
	
	joined = []

	for csv_filepath in filepaths:
		with open(csv_filepath) as f:
			processed_data = [{k: str(v) for k, v in row.items()}
			for row in csv.DictReader(f, skipinitialspace=True)]
		joined += processed_data
	
	joined_sorted = sorted(joined, key=lambda k: k["account_name"])
	
	keys = joined_sorted[0].keys()
	with open(csv_output, 'wb') as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(joined_sorted)

else:
	print("Inputs needed. Need datapath1, datapath2, datapath3 ... , datapathN, outputpath.")
