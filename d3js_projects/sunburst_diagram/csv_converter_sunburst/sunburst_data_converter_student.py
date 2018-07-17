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
#	Want to make a sunburst diagram that  
#
#	FINAL OUTPUT:
#
#		node -> { name, value, children }
#		children -> [ nodes ]

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

	weekNum = 0	
	if(sys.argv[1]):
		weekNum = sys.argv[1]
	else:
		weekNum = -1

	fileName = fileProto + weekNum + fileProtoEnd

	if weekNum != -1:
	
		# open file
		with open(fileName) as ifp:

			#data.append( { str(weekNum) : [] } )
			week = csv.reader(ifp)
		
			for student in week:
			
				# split student sequences
				studentSeq = student[0].split(' ')
				data.append( studentSeq[ 1 : len(studentSeq) - 1] )

		return data

	else:
		return -1


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
		
	fileName = "student_seq_week/student_seq_week_" + str(sys.argv[1]) + ".json"

	with open(fileName, 'w') as outfile:
		json.dump(res, outfile)

	

def main( ):

	# error prevention
	if(not sys.argv[1]):
		print("Please enter a file tag as second argument")
		return 0

	# Read in and write out the data from a csv
	writeOut( readIn() )

	
# so let's roll
main()
