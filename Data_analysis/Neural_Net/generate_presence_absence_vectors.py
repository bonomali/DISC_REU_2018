#!/usr/bin/python
import numpy as np
import csv
import json
import matplotlib.pyplot as plt
import sys
sys.path.append("../HON_Creation/")
from jianxu_main import fast_build_HON
from os import listdir
from os.path import isfile, join

##  Generate HON nodes for each assignment
sequence_path = "../../Raw_data_processing_JSON_to_CSV/Sequence_Data"
seqfiles = [f for f in listdir(sequence_path) if isfile(join(sequence_path, f))]

for f in seqfiles:
	if "clicks" in f:
		fast_build_HON(MinSupport = 10, MaxOrder= 99, Freq = False, Input_Sequence_File = sequence_path + "/" + f, OutputNetworkFile = "HON_Files/HON_"+f[:-11]+".csv")	

##  Get a list of all nodes
HON_path = "HON_Files"
HONfiles = [f for f in listdir(HON_path) if isfile(join(HON_path, f))]

nodes = []
for f in HONfiles:
	HON_data = np.loadtxt(HON_path + "/" + f, dtype = str, delimiter = ",", skiprows = 1)
	for line in HON_data:
		nodes.append(line[0])
		nodes.append(line[1])

##  Use set() to remove duplicate entries
nodes = list(set(nodes))
node_vector = []

##  Loop over each node to reverse the order + remove "." and "|"
##  because the node "13|4.5" corresponds to the sequence " 4 5 13 "
for node in nodes:
	elements = []
	start = 0
	for index in range(len(node)):
		if node[index] == "|" or node[index] == ".":
			elements.append(node[start:index])
			start = index +1
	elements.append(node[start:])
	reversed_elements = list(reversed(elements))
	node_sequence = ""
	for element in reversed_elements:
		node_sequence += " " +element
	node_sequence += " "
	if node_sequence[0] == " " and node_sequence[1] == " ":
		node_sequence = node_sequence[1:]
	node_vector.append(node_sequence)

print("# nodes = " + str(len(node_vector)))
##  Generate the results for each assignment
grades_file = "grades.csv"
grades = {}
with open('grades.csv', newline='') as grades_file:
	reader = csv.DictReader(grades_file)
	for row in reader:
		results = {}
		for key in list(row.keys()):
			if not key == "NetID":
				results[key] = row[key]
			grades[row["NetID"]] = results


totals = grades["Total"]
filtered_grades = {}

for name in list(grades.keys()):
	if name != "Total":
		filtered_grades[name] = {}
		for assignment in list(grades[name].keys()):
			if grades[name][assignment] != "":
				score = float(grades[name][assignment])
			else:
				score = 0.
			total = float(totals[assignment])
			percent = score/total
			filtered_grades[name][assignment] = percent

##  Generate our presence / absence vector for each entry
def vector_gen(sequence, vector):
	absence_vector = [0]*len(vector)
	for index in range(len(vector)):
		if vector[index] in sequence:
			absence_vector[index] = 1
	return absence_vector 

perfect = 0
not_perfect = 0
training_data = {}
test_data = {}

training_perf = 0
test_perf = 0
training_imperf = 0
test_imperf = 0

for f in seqfiles:
	if "clicks" in f:
		vectors_training = {}
		vectors_test = {}
		with open(sequence_path + "/" + f, "r") as ins:
			for line in ins:
				name = line.split(" ", 1)[0]
				assignment = f[8:-11]
				if name in list(filtered_grades.keys()) and assignment in list(filtered_grades[name].keys()):
					grade = filtered_grades[name][assignment]
					sequence = " " + line.split(" ", 1)[1][:-1] + " "
					if grade != 1.0:
						not_perfect +=1
						if not_perfect == 5:
							vectors_test[name] = {"vector":vector_gen(sequence, node_vector), "percentage":"%.1f" % grade}
							not_perfect = 0
							test_imperf +=1
						else:
							vectors_training[name] = {"vector":vector_gen(sequence, node_vector), "percentage":"%.1f" % grade}
							training_imperf +=1
					else:
						perfect += 1
						if perfect == 5:
							vectors_test[name] = {"vector":vector_gen(sequence, node_vector), "percentage":"%.1f" % grade}
							perfect = 0
							test_perf +=1
						else:
							vectors_training[name] = {"vector":vector_gen(sequence, node_vector), "percentage":"%.1f" % grade}
							training_perf +=1
		training_data[assignment] = vectors_training
		test_data[assignment] = vectors_test

print("# 100% training count =" + str(training_perf))
print("# 100% test count =" + str(test_perf))
print("# negative training count =" + str(training_imperf))
print("# negative test count =" + str(test_imperf))


with open('training_vectors.json', 'w') as fp:
	json.dump(training_data, fp, sort_keys=True)

with open("test_vectors.json", "w") as fp:
	json.dump(test_data, fp, sort_keys = True)

master_vector = {"Master":node_vector}
with open('master_vector_new.json', 'w') as fp:
	json.dump(master_vector, fp, sort_keys=True)


"""
## To use this data elsewhere, use the following:
with open('presence_vectors.json', 'r') as fp:
	data = json.load(fp)
"""
