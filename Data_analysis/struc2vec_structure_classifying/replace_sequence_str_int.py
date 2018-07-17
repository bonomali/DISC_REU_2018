###Must replace each unique node string with an integer value so that struc2vec will actually work
import networkx as nx
import csv
import numpy as np
import sys

def replace_sequence_str_int(HON_dir = "../HON_Creation/",
							 reference = "object-ref_order",
							 int_file = 'int-network-cell_order',
							 MinSupport = 8, MaxOrder = 99, out_file_add = ''):
		
	#  Adds the HON python scripts to your system directory so that they can be imported
	sys.path.append(HON_dir)
	from jianxu_main import fast_build_HON
	fast_build_HON(MinSupport = MinSupport, MaxOrder= MaxOrder, Freq = False)	
	
	#  first create a list with every object id
	HON_file = 'network-cell-maxorder-'+str(MaxOrder)+ "MinSupport-"+ str(MinSupport) +str(out_file_add) +'.csv'
	
	reference_csv = reference + str(MaxOrder) + ".csv"
	int_file = int_file + str(MaxOrder) + ".csv"
	network_data = np.genfromtxt(HON_file, delimiter=',',dtype=('U100', 'U100', float), skip_header=1)
	
	objects = []
	for line in network_data:
		nodeleft = line[0]
		noderight = line[1]
		objects.append(nodeleft)
		objects.append(noderight)
	
	#  identify only unique object ids
	object_types = list(set(objects))
	
	#  make a dictionary with key:value pairs of object_id : ref_number
	object_ref = {}
	for index in range(len(object_types)):
		object_ref[object_types[index]] = str(index)
	
	#  now, rewrite the edgelist using the object_ref numbers
	
	int_data = []
	for line in network_data:
		nodeleft = line[0]
		nodeleft_int = object_ref[nodeleft]
		noderight = line[1]
		noderight_int = object_ref[noderight]
		weight = line[2]
		newline = [nodeleft_int, noderight_int, weight]
		int_data.append(newline)
	
	with open(reference_csv, 'w') as csv_file:
		writer = csv.writer(csv_file)
		for key, value in object_ref.items():
			writer.writerow([key, value])
	
	with open(int_file, 'w') as csv_file:
		writer = csv.writer(csv_file)
		for key, value, weight in int_data:
			writer.writerow([key, value, weight])
