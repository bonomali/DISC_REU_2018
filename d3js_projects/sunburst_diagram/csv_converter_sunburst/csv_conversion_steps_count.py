import csv

# turn csv into diction 
nodes = {};

#First, load in the modularity classes dictionary
with open('network-cell.csv' , newline='') as f:
	next(f)  # Skip the header

	# reader is an array of arrays
	# ['source' , 'target' , 'value']
	reader = csv.reader(f, skipinitialspace=True)

	# make a dictionary of nodes with their values	
	for elem in reader:
		print(elem)

		# add up number of instances of node
		# by adding all times where node was target
		if(elem[1] not in nodes):
			nodes[ elem[1] ] = int(elem[2])
		else:
			nodes[ elem[1] ] = int(elem[2])

	# find source nodes ( should only be the ones where they end in a | )
	sourceNodes = {};
	for key in nodes.keys():
		if key[ -1 ] == '|':
			sourceKey = key[ : len(key) - 1] # remove the bar
			sourceNodes[ sourceKey ] = nodes[key]

	print(sourceNodes)

	# find out how many trails began with 2
	#for key in nodes.keys():
		#if key[ len(key) - 2 : len(key) ] == ".2":
			#print(key)

# write data out to a csv
	#writer = csv.writer(open("sunburst_data.csv", 'w'))
	#	for row in data:
	#	writer.writerow(row)
