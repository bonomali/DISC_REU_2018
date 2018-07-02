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

# file names
ALL_DATA = "SP18_all_data.csv"
OBJECT_REF_TYPES = "object_ref_types.csv"
SEQUENCES = "sequence.txt"
OUTPUT_FILE = "SP18_all_data_v2.csv"

def processAllData():
	
	# const indices for the reader
	ACCOUNT = 6
	WEEK    = 0
	DATE    = 5
	TIME    = 4
	URL     = 2

	# read in data as a list
	data = []

	with open(ALL_DATA , 'rb') as ifp:

		for row in csv.reader(ifp):
			data.append( [ row[ACCOUNT] , row[WEEK] , row[DATE] , row[TIME] , row[URL] ])

	return data

def processObjRef():
	
	# const indices for the reader
	URL     = 0
	URL_NUM = 1
	TYPE    = 2

	# read in data as a list
	data = []
	with open(OBJECT_REF_TYPES , 'rb') as ifp:
		for row in csv.reader(ifp):

			# get assignment name
			assignment = ( ( row[URL].split('/') )[-1].split('.') )[0]

			data.append( [ assignment , row[URL_NUM] , row[TYPE] , row[URL] ] )
	
	return data

def combineData( allData , objectRef ):
	
	# change header
	allData = allData[ 1 : ]

	# clear all urls
	for student in allData:
		for assignment in objectRef:

			# check for coursework
			if "Coursework" in student[4]:
				student[4] = "Coursework"
				student.append( assignment[1] )
				student.append( assignment[2] )

			# check for equivalent url
			elif assignment[3] == student[4]:

				student[4] = assignment[0]
				student.append( assignment[1] )
				student.append( assignment[2] )
				
	# now the list is formatted as
	# account,week,date,time,assignment,url_num,type

	return allData
	
def outputToCSV( data ):

	with open(OUTPUT_FILE , 'wb') as ofp:
		fieldnames = ['account', 'week' , 'date' , 'time' , 'assignment' , 'url_num' , 'type']
		writer = csv.DictWriter(ofp, fieldnames=fieldnames)
		writer.writeheader()
		for row in data:
			writer.writerow( { 'account':row[0] , 'week':row[1] , 'date':row[2] , 'time':row[3] , 'assignment':row[4] , 'url_num':row[5] , 'type':row[6] } )

def main():

	# process the data for each file
	allData = processAllData()
	objectRef = processObjRef()

	# combine necessary data
	totalData = combineData( allData , objectRef )


	# output to csv
	outputToCSV( totalData )

main()
