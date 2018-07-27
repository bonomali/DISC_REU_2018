import csv

with open('sequence.txt', 'r') as in_file:
	data = []
	for line in in_file:
		newLine = line.replace( ' ' , ',' , 1 ).replace(' ' , '-' )
		if newLine[-1] == '-':
			newline[-1] = ''
		data.append( newLine )

	f = open('sequence.csv','w')
	f.write('name,sequence\n')
	for datum in data:
		f.write( datum )
	f.close()
