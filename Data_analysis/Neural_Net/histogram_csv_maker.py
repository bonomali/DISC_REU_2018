#!/usr/bin/python
import numpy as np
import csv, json, sys
import matplotlib.pyplot as plt
sys.path.append("../HON_Creation/")
from jianxu_main import fast_build_HON
from os import listdir
from os.path import isfile, join



##  Function to generate presence / absence vector for each entry
def vector_gen(sequence, nodes_vector, nature="structure"):
	if nature == "structure":
		struc_vector = struc128D
		struc_type="struc2vec128D"
	else:
		struc_vector = community
		struc_type = "community"
	absence_vector = [0]*len(struc_vector)
	for index in range(len(nodes_vector)):
		if nodes_vector[index] in sequence:
			count = sequence.count(nodes_vector[index])
			struc = data[nodes[index]][struc_type]
			absence_vector[struc_vector.index(struc)] +=count
	return absence_vector 



##  Define function that generates histogram files, then run for both community and structure classifications
def write_stacked_histogram_files(students_data, nature = "structure"):
	# Change the type of classification being read:
	if nature == "structure":
		struc_vector = struc128D
		struc_type="struc2vec128D"
		vector_name = "struc_vector"
	else:
		struc_vector = community
		struc_type = "community"
		vector_name = "community_vector"
	
	###  Now, rewrite data in the correct format for the stacked histogram, i.e. in a csv table	
	header = "student_assignment_grade"
	for index in range(len((struc_vector))):
		header += "," + "struc"+struc_vector[index]
	
	name_number = 0
	with open('histogram_'+nature+'.csv','w') as f:
		f.write(header)
		f.write("\n")
		for name in list(students_data.keys()):
			name_number += 1
			for assignment in list(students_data[name].keys()):
				line = "student"+str(name_number)+"_"+assignment+"_"+students_data[name][assignment]["grade"]
				for structure in students_data[name][assignment][nature]:
					line+=","+str(structure)
				f.write(line)
				f.write('\n')

	### Next, record the average data for each grade band (aggregate view)
	summed_data = {}
	grade_counts = {}
	for assignment in list(training_data.keys()):
		data = training_data[assignment]
		for student in list(data.keys()):
			students_data = data[student]
			grade = students_data["percentage"]
			classifications = students_data[vector_name]
			try:
				summed_data[str(grade)] += np.asarray(classifications)
				grade_counts[str(grade)] += 1
			except:
				summed_data[str(grade)] = np.asarray(classifications)
				grade_counts[str(grade)] = 1

	average_data = {}
	for grade in list(summed_data.keys()):
		#Need at least five entries in a grade band to include it; otherwise you'll get data that isn't very useful.
		if grade_counts[grade] >=5:
			average_data[grade] = summed_data[grade]/grade_counts[grade]#sum(summed_data[grade])

	header = "grade"
	for index in range(len((struc_vector))):
		header += "," + "struc"+struc_vector[index]

	###  Now, rewrite data in the correct format for the stacked histogram, i.e. in a csv table
	with open('grades_'+nature+'.csv','w') as f:
		f.write(header)
		f.write("\n")
		for grade in sorted(list(average_data.keys())):
			line = grade
			for structure in average_data[grade]:
				line+=","+str(structure)
			f.write(line)
			f.write('\n')







## define some variables to store data in:
nodes=[]
struc2vec128D = []
community = []
data = {}

##  Load up HON nodes and classifications
data_path = "../classifying_nodes/fdd_nodes.csv"
sequence_path = "../../Raw_data_processing_JSON_to_CSV/Sequence_Data"
seqfiles = [f for f in listdir(sequence_path) if isfile(join(sequence_path, f))]

with open(data_path,'r') as f:
	fieldnames = ['sequence', 'struc2vec128D', 'struc2vec2D', 'community']
	reader = csv.DictReader(f, fieldnames=fieldnames, )
	next(reader, None)
	for row in reader:
		nodes.append(row["sequence"])
		struc2vec128D.append(row["struc2vec128D"])
		community.append(row["community"])
		data[row["sequence"]] = {"struc2vec128D":row["struc2vec128D"], "community":row["community"]}


##  Use set() to remove duplicate entries. Will use these vectors to generate presence / absence vectors to sum up for histogram.
struc128D = list(set(struc2vec128D))
struc128D = sorted(struc128D)

community = list(set(community))
community = sorted(community)

##  Loop over each node to reverse the order, and also to remove "." and "|"
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

##  Generate the grades for each assignment
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


## Use the following to ensure a consistent 1:4 ratio of test:training data, with equal proportions of perfect / non-perfect scores in each.
## Don't need to separate training / test data unless you want to test prediction capability 
## If you want training data / test data separated, uncomment the +=1 lines in the following for loop. Otherwise it will all enter training data.
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
						#not_perfect +=1
						if not_perfect == 5:
							vectors_test[name] = {"struc_vector":vector_gen(sequence, node_vector, nature="structure"),
												  "community_vector":vector_gen(sequence, node_vector, nature="community"), "percentage":"%.1f" % grade}
							not_perfect = 0
							test_imperf +=1
						else:
							vectors_training[name] = {"struc_vector":vector_gen(sequence, node_vector, nature="structure"),
													  "community_vector":vector_gen(sequence, node_vector, nature="community"), "percentage":"%.1f" % grade}
							training_imperf +=1
					
					else:
						#perfect += 1
						if perfect == 5:
							vectors_test[name] = {"struc_vector":vector_gen(sequence, node_vector, nature="structure"), 
												  "community_vector":vector_gen(sequence, node_vector, nature="community"), "percentage":"%.1f" % grade}
							perfect = 0
							test_perf +=1
						else:
							vectors_training[name] = {"struc_vector":vector_gen(sequence, node_vector, nature="structure"), 
													  "community_vector":vector_gen(sequence, node_vector, nature="community"), "percentage":"%.1f" % grade}
							training_perf +=1
		training_data[assignment] = vectors_training
		test_data[assignment] = vectors_test



###  Write the stacked-histogram csv files now
###  First off, record an individual student's results across the assignments, broken down into struc proportions
###  data is initially stored in the format arranged_data = {"student_id": {"assignmentname": {"grade":1.0, "structures":[1,2,1,0...]}, ...]}
###  Use for student comparison view
arranged_data = {}
for	assignment in list(training_data.keys()):
	data = training_data[assignment]
	for student in list(data.keys()):
		student_data = data[student]
		grade = student_data["percentage"]
		structures = student_data["struc_vector"]
		communities = student_data["community_vector"]
		try:
			arranged_data[student][assignment] = {"grade":grade}
		except:
			arranged_data[student] = {}
			arranged_data[student][assignment] = {"grade":grade}
		arranged_data[student][assignment]["structure"] = structures
		arranged_data[student][assignment]["community"] = communities



write_stacked_histogram_files(arranged_data, nature = "structure")
write_stacked_histogram_files(arranged_data, nature = "community")
