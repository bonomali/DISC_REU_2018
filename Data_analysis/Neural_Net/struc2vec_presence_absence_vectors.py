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

##  Load up HON nodes and classifications
data_path = "../classifying_nodes/struc2vec-directed-classified-499.csv"
sequence_path = "../../Raw_data_processing_JSON_to_CSV/Sequence_Data"
seqfiles = [f for f in listdir(sequence_path) if isfile(join(sequence_path, f))]

nodes=[]
struc2vec2D = []
struc2vec128D = []
data = {}

with open(data_path,'r') as f:
	fieldnames = ['sequence', 'struc2vec128D', 'struc2vec2D', 'node2vec128D', 'node2vec2D']
	reader = csv.DictReader(f, fieldnames=fieldnames, )
	next(reader, None)
	for row in reader:
		nodes.append(row["sequence"])
		struc2vec2D.append(row["struc2vec2D"])
		struc2vec128D.append(row["struc2vec128D"])
		data[row["sequence"]] = {"struc2vec2D":row["struc2vec2D"], "struc2vec128D":row["struc2vec128D"], "node2vec2D":row["node2vec2D"], "node2vec128D":row["node2vec128D"]}


##  Use set() to remove duplicate entries
struc2D = list(set(struc2vec2D))
struc128D = list(set(struc2vec128D))
struc128D = sorted(struc128D)
##  Loop over each node to reverse the order + remove "." and "|"
##  because the node "13|4.5" corresponds to the sequence " 4 5 13 "
node_vector=[]
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
def vector_gen(sequence, nodes_vector, struc_vector = struc128D, struc_type="struc2vec128D"):
	absence_vector = [0]*len(struc_vector)
	for index in range(len(nodes_vector)):
		if nodes_vector[index] in sequence:
			count = sequence.count(nodes_vector[index])
			struc = data[nodes[index]][struc_type]
			absence_vector[struc_vector.index(struc)] +=count
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
					if grade > 1.0:
						grade = 1.0
					if grade <= 1.0:
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


with open('struc128D_training_vectors.json', 'w') as fp:
	json.dump(training_data, fp, sort_keys=True)

with open("struc128D_test_vectors.json", "w") as fp:
	json.dump(test_data, fp, sort_keys = True)

master_vector = {"Master":struc128D}
with open('struc128D_master_vector.json', 'w') as fp:
	json.dump(master_vector, fp, sort_keys=True)


"""
## To use this data elsewhere, use the following:
with open('presence_vectors.json', 'r') as fp:
	data = json.load(fp)
""" 


###  Write the stacked-histogram csv files while you're at it...
###  First off, record an individual student's results across the assignments, broken down into struc proportions
###  data is initially stored in the format arranged_data = {"student_id": {"assignmentname": {"grade":1.0, "structures":[1,2,1,0...]}, ...]}
arranged_data = {}
for assignment in list(training_data.keys()):
	data = training_data[assignment]
	for student in list(data.keys()):
		student_data = data[student]
		grade = student_data["percentage"]
		structures = student_data["vector"]
		try:
			arranged_data[student][assignment] = {"grade":grade}
		except:
			arranged_data[student] = {}
			arranged_data[student][assignment] = {"grade":grade}
		arranged_data[student][assignment]["structures"] = structures

header = "student_assignment_grade"
for index in range(len((struc128D))):
	header += "," + "struc"+struc128D[index]

###  Now, rewrite data in the correct format for the stacked histogram, i.e. in a csv table
name_number = 0
with open('histogram.csv','w') as f:
	f.write(header)
	f.write("\n")
	for name in list(arranged_data.keys()):
		name_number += 1
		for assignment in list(arranged_data[name].keys()):
			line = "student"+str(name_number)+"_"+assignment+"_"+arranged_data[name][assignment]["grade"]
			for structure in arranged_data[name][assignment]["structures"]:
				line+=","+str(structure)
			f.write(line)
			f.write('\n')

### Next, record the average data for each grade band.
summed_data = {}
grade_counts = {}
for assignment in list(training_data.keys()):
	data = training_data[assignment]
	for student in list(data.keys()):
		student_data = data[student]
		grade = student_data["percentage"]
		structures = student_data["vector"]
		try:
			summed_data[str(grade)] += np.asarray(structures)
			grade_counts[str(grade)] += 1
		except:
			summed_data[str(grade)] = np.asarray(structures)
			grade_counts[str(grade)] = 1

average_data = {}
for grade in list(summed_data.keys()):
	if grade_counts[grade] >=5:
		average_data[grade] = summed_data[grade]/grade_counts[grade]#sum(summed_data[grade])

print(grade_counts)
header = "grade"
for index in range(len((struc128D))):
	header += "," + "struc"+struc128D[index]

###  Now, rewrite data in the correct format for the stacked histogram, i.e. in a csv table
with open('grade_structures.csv','w') as f:
	f.write(header)
	f.write("\n")
	for grade in sorted(list(average_data.keys())):
		line = grade
		for structure in average_data[grade]:
			line+=","+str(structure)
		f.write(line)
		f.write('\n')
