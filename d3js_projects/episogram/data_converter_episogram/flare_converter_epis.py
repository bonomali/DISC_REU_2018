# FILE FORMAT:
# 
# { root : 
#			[ { student :
#						[ { weeks :
#									[ { assignments:
#													[ date , time , url_num , name ] }]}]}]}


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
	
	return res

def readIn( ifp ):
	""" Creates an array of objects from data """

	data = {}

	#First, load in the modularity classes dictionary
	with open(ifp) as f:
		next(f)  # Skip the header

		# reader is an array of arrays
		# ['node' , 'group']
		reader = csv.reader(f, skipinitialspace=True)

		# make a dictionary of students with arrays of assignments	
		c = 0
		for elem in reader:
			

			assignment = { 	"week": elem[1] , "date": elem[2] , "time":elem[3] , "name":elem[4] , "url_num":elem[5] , "type":elem[6] }

			# limit file size for mini set
			if( len(data.keys()) < 20):

				# if there is a new name, create an array of assignment objects for it
				if( elem[0] not in data.keys() ):
					data[ elem[0] ] = [ assignment ] 
					c += 1

				# add on to an existing array
				else:
					data[ elem[0] ].append( assignment )

	return data

def writeOut( data ):

	# printing results into the terminal
	import json
	with open('episogram_data_mini.json', 'w') as outfile:
		json.dump(data, outfile)

	

def main():

	# read in data and format
	writeOut( readIn("SP18_all_data_v2.csv") )
	
# so let's roll
main()
