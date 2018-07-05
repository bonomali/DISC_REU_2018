"""
	Using SP18_all_data_v2.csv , create an array of week objects
	where each week holds an array of assignment objects

	input file:  SP18_all_data_v2.csv
	output file: assignments_by_week.json

"""

#!/usr/bin/python

import csv
import json
import sys
import datetime as dt

# file names
ALL_DATA = "SP18_all_data_v2.csv"
OUTPUT_FILE = "assignments_by_week.json"

def processAllData():
	
	# const indices for the reader
	ACCOUNT = 0
	WEEK    = 1
	DATE    = 2
	TIME    = 3
	ASSIGN  = 4
	URL_NUM = 5
	TYPE    = 6

	processedData = []
	num_weeks = -1

	with open(ALL_DATA , 'rb') as ifp:

		# find number of week objects to be made
		reader = csv.reader(ifp)
		next(reader, None)  # skip the headers

		for row in reader:
			
			if( int(row[1]) > num_weeks ):
				num_weeks = int(row[1])
			
		# make empty week 'objects' array
		for i in range( num_weeks + 1 ) :
			processedData.append( { str(i) : [] } )

		print(processedData)


	with open(ALL_DATA , 'rb') as ifp:

		# group all assignments by week
		reader = csv.reader(ifp)
		next(reader , None)  # skip the headers

		print( "Processing data..." )

		for row in reader:
			for week in processedData:

				# add assignments of mathing week
				if int( row[1] ) == int( week.keys()[0] ):
					week[ week.keys()[0] ].append( row )


		print("Processing complete.")

	return processedData



def outputToJSON( data ):

	print("Writing data to file...")

	# output data to file
	import json
	with open(OUTPUT_FILE, 'w') as outfile:
		json.dump(data, outfile)

	print("Writing completed")


def main():

	# process the data for each file
	allData = processAllData()


	# output to json
	outputToJSON( allData )

main()
