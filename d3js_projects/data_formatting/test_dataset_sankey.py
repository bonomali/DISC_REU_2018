# make a test dataset for sankey diagram given nodes in nodes_classified.csv
# each node should go to a number of 5 grades: A, B, C, D, F

import csv
import random

INPUT_FILE = "nodes_classified.csv"
OUTPUT_FILE = "dummy_grades.csv"

GRADES = [ "A" , "B" , "C" , "D" , "F" ]

data = [ ["source" , "target" , "value"] ]

# read in data
with open(INPUT_FILE , 'rb') as ifp:
	reader = csv.reader(ifp)

	next(reader, None)  # skip the headers
	for row in reader:

		node = row[0]

		# add a random value, then a grade target
		for grade in GRADES:
			
			# make a random value 1 - 5
			data.append( [ node , grade , str( random.randint(1,5)) ] )

# write out data
with open(OUTPUT_FILE , 'w') as ofp:
	writer = csv.writer(ofp)
	writer.writerows(data)

