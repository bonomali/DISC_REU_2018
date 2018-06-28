###Must replace each unique node string with an integer value so that struc2vec will actually work
import networkx as nx
import csv
import numpy as np


network_file = "weights-network-cell.csv"

network_data = np.genfromtxt(network_file, delimiter=',',dtype=('U100', 'U100', float))


#  first create a list with every object id
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
	newline = [nodeleft_int, noderight_int]
	int_data.append(newline)

with open('object_ref.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in object_ref.items():
       writer.writerow([key, value])

with open('int-network-cell.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in int_data:
       writer.writerow([key, value])
