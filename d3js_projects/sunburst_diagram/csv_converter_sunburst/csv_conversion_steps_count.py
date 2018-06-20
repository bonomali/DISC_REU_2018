import csv
import json

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# repeatSource() compares a node path to a previously established
#				 travel path, then adds a new branch
# input:		 node;   travel path of node
#                source; original travel paths branch
# output:        returns a full branch of paths
def repeatSource( node , source ):
	# BASE CASE: found a different item
	if type(source) != dict:
		print('weird')
		return source
		
	elif node[ -1 ] not in source.keys():
		print('base')
		return getChild( node )

	# RECURSIVE CASE
	else:
		print( list(source.keys()) )
		return repeatSource( node[ : -1] , source[ list(source.keys())[0] ] )	

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# getChild() formats the hierarchy for a node sequence
#			 ie: { node: { node: { node: { node : '' } } } }
# Input:     node; a list of sequence data
# Output:    a dictionary organized sequence
def getChild( node ):
	# BASE CASE: last item
	if len(node) == 1:
		return node[0]

	# RECURSIVE CASE
	else:
		return { node[-1] : getChild( node[ : -1 ] ) }


#######################################################################

# turn csv into dictionary for json

data = []

#First, load in the modularity classes dictionary
with open('nodes_classified.csv' , newline='') as f:
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
		#node = node.replace('.' , ',')

		# add to list
		data.append(node)
	
	print(data)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	'''
	# put all sources together (recursively do until stop?)
	sourceNodes = {}
	for node in data:
		source = node[ -1 ]

		# for a new source, create sequence
		if source not in sourceNodes.keys():
			sourceNodes[ source ] = getChild( node )

			if sourceNodes[ source ] == str( sourceNodes[ source ] ):
				sourceNodes[ source ] = { source : '' }

		# if source was a string and found twice, add and make object
		elif sourceNodes[source] == source:
			sourceNodes[ source ] = getChild( node )

		# if a source is repeated, branch paths
		else:			
			sourceNodes[source] = repeatSource( node , sourceNodes[source] )


	for node in sourceNodes.keys():
		print( sourceNodes[node] )
	'''
# write data out to a csv
writer = csv.writer(open("sunburst_data.csv", 'w'))
for row in data:
	writer.writerow(row)
