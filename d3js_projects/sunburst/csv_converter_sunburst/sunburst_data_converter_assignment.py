# File: sunburst_csv_converter.py
# Author: Eric Gronda
# Date: 6/22/18
# Description:
# 		Converts nodes_classified.csv to json format for 
#		combatibility with sunburst diagram
# References:
#		User "Hett"'s comment on: 
#		https://stackoverflow.com/questions/43757965/convert-csv-to-json-tree-structure

########################################################################################
#	FINAL OUTPUT:
#
#		node -> { name, value, children }
#		children -> [ nodes ]

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
	Make a sunburst of assignments for each week in the semester
	Each student has assignment blocks that change opacity based on number of clicks
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import sys
import csv
from collections import defaultdict


def ctree():
	""" One of the python gems. Making possible to have dynamic tree structure.

	"""
	return defaultdict(ctree)


def build_leaf(name, leaf):
	""" Recursive function to build desired custom tree structure

	"""
	res = {"name": name}
	# add children node if the leaf actually has any children
	if len(leaf.keys()) > 0:
		res["children"] = [build_leaf(k, v) for k, v in leaf.items()]
	
	# set a size for the nodes
	else:
		res["size"] = 1  # 1 person per node
	

	return res

def readIn():

	# make an array of data to return
	data = []

	# sequences by week (place weekNum between fileProto and fileProtoEnd)
	fileProto = "../../../Raw_data_processing_JSON_to_CSV/sequence"
	fileProtoEnd = ".txt"

	for weekNum in range( 3 , 20 ):
		fileName = fileProto + str(weekNum) + fileProtoEnd
		assignName = "Assignment " + str(weekNum)

		# open file
		with open(fileName) as ifp:
			week = csv.reader(ifp)
		
			for student in week:
			
				# count number of clicks per assignment 
				studentName = student[0][0]
				numClicks   = len( (student[0].split(' '))[ 1 : len((student[0].split(' '))) - 1])

				data.append( { studentName , numClicks , assignName } )

	return data


def writeOut( data ):
	""" The main thread composed from two parts.

	First it's parsing the csv file and builds a tree hierarchy from it.
	Second it's recursively iterating over the tree and building custom
	json-like structure (via dict).

	And the last part is just printing the result.

	"""


	tree = ctree()

	for rid, row in enumerate(data):

		# skipping first header row. remove this logic if your csv is
		# headerless
		if rid == 0:
			continue

		# usage of python magic to construct dynamic tree structure and
		# basically grouping csv values under their parents
		leaf = tree[row[0]]
		for cid in range(1, len(row)):
			leaf = leaf[row[cid]]

	# building a custom tree structure
	res = []
	for name, leaf in tree.items():
		res.append(build_leaf(name, leaf))

	
	# adding root node
	res = { "name":"root" , "children":res }


	# outputs to json file
	# makes student sequence file
	import json
		
	fileName = "student_seq_week/student_assigns_" + str(sys.argv[1]) + ".json"

	with open(fileName, 'w') as outfile:
		json.dump(res, outfile)

	

def main( ):

	# Read in and write out the data from a csv
	data = readIn()
	if( data ):
		writeOut( data )

	
# so let's roll
main()
