import collections
import csv
import json

def buildHierarchy( arr2D ):
	"""
		This is the method suggested by kyle... does not branch out

	"""

	hierarchy = { "name":"root" , "children":[] }

	# go through each row
	for row in arr2D:
		subHier = hierarchy

		# go through each item
		for index , item in enumerate(row):

			# make a new child object that only 
			# has children if not the end of sequence
			newDict = {}
			if index != len(row) - 1: 
				newDict = { "name":str(item) , "children":[] }
			else:
				newDict = { "name":str(item) , "size":1 } 

			# add new children to level
			if item not in subHier["children"]:
				subHier["children"].append( newDict )
				
			# go through the children and switch to that child
			for child in subHier["children"]:
				if child["name"] == str(item):
					subHier = child

	# output data
	print json.dumps(hierarchy, sort_keys=True, indent=4, separators=(',', ': '))

	with open('sunburst_data_v3.json', 'w') as outfile:
		json.dump(hierarchy, outfile)

def readIn():
	""" Reads in a list of nodes from csv and separates it by sequence """

	ifp = "struc2vec-directed-weighted-classified.csv" 
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

			# convert all to strings
			for point in node:
				point = str(point)

			# add to list
			data.append(node)

	return data


def add_element(root, path, data):
	"""
		lambda: simplified function
			format: lambda input1 , input2 , ... : function

		reduce(): goes through all elements of the list 

	"""
	
    reduce(lambda x, y: x[y], path[:-1], root)[path[-1]] = data

def main():
	tree = lambda: collections.defaultdict(tree)
	root = tree()

	data = readIn()

	try:
		for row in data:
			add_element(root, row, 1)
	except:
		pass

	# printing results into the terminal
	#print json.dumps(root, sort_keys=True, indent=4, separators=(',', ': '))

	with open("sunburst_data_v3.json" , "w") as ofp:
		json.dump(root , ofp)

main()
