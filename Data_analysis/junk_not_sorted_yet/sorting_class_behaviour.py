import matplotlib.pyplot as plt

import networkx as nx
import csv
import numpy as np

import re

##Open up data
network_file = "d3js_projects/nodes_classified.csv"
sequence_data = np.genfromtxt(network_file, delimiter=',', names = True, dtype=['U100',float])

##Filter into a list of websites included in the sequence based on modularity class
class_data = []
for clas_num in range(16):
	sequences = []
	mod_filtered = [item for item in sequence_data if item[1] == clas_num]
	print(mod_filtered)
	for sequence in mod_filtered:
		strng = sequence[0]
		strng= re.findall('\d+', strng )
		sequences.append(strng)
	
	class_data.append(sequences)


for class_num in range(16):
	fig, ax = plt.subplots()
	length = len(class_data[class_num])
	print(length)
	counter = 0
	for sequence in class_data[class_num]:
		y = list(map(int, sequence))
		x = np.arange(len(sequence))
		plt.plot(x, y, label='pre (default)', alpha=0.1, color='black')
		plt.scatter(x, y, alpha=0.1, color='black')
		plt.ylim(0, 37)
		counter +=1

