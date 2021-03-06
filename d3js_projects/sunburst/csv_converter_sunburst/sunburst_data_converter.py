# File: sunburst_csv_converter.py
# Author: Eric Gronda
# Date: 6/22/18
# Description:
# 		Converts nodes_classified.csv to json format for 
#		combatibility with sunburst diagram
# References:
#		User "Hett"'s comment on: 
#		https://stackoverflow.com/questions/43757965/convert-csv-to-json-tree-structure

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

def readIn( ifp ):
	""" Reads in a list of nodes from csv and separates it by sequence """

	data = []

	#First, load in the modularity classes dictionary
	with open(ifp) as f:
		next(f)  # Skip the header

		# reader is an array of arrays
		# ['node' , 'group']
		reader = csv.reader(f, skipinitialspace=True)

		# make a list of nodes with their values	
		for elem in reader:
			# format elements
			node = elem[0].replace('|' , '.')
			node = node[ : -1 ] if node[-1] == '.' else node
			node = node.split('.')
			node = node[::-1]
			#node = node.replace('.' , ',')

			# add to list
			data.append(node)

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

	
	"""
	# NOTE: you need to have test.csv file as neighbor to this file
	with open('sunburst_data.csv') as csvfile:
		reader = csv.reader(csvfile)
		for rid, row in enumerate(reader):

			# skipping first header row. remove this logic if your csv is
			# headerless
			if rid == 0:
				continue

			# usage of python magic to construct dynamic tree structure and
			# basically grouping csv values under their parents
			leaf = tree[row[0]]
			for cid in range(1, len(row)):
				leaf = leaf[row[cid]]

	"""

	# building a custom tree structure
	res = []
	for name, leaf in tree.items():
		res.append(build_leaf(name, leaf))

	
	# adding root node
	res = { "name":"root" , "children":res }


	# printing results into the terminal
	import json
	with open('sunburst_data_struc2vec.json', 'w') as outfile:
		json.dump(res, outfile)

	

def main():

	# Read in and write out the data from a csv
	writeOut( readIn( "weights-network-cell.csv" ) )

	
# so let's roll
main()
