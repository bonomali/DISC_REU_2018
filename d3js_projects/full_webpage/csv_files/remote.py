from scipy.stats import entropy
import numpy as np
import csv
import json
dict = {"Capstone":0,"ePortfolio Link":1,"Integration3":2,"Prompt1":3,"Prompt2":4,
  "Prompt3":5,"Prompt4":6,"Prompt5":7,"Prompt6":8,"Prompt7":9,"Prompt8":10,
  "Prompt9":11,"Prompt10":12,"Prompt11":13}
  
def data_filter(number):
	vector = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	name = "student"+str(number)
	for line in file_data:
		arr = line[0].split('_')
		if arr[0] == name:
			no = dict[arr[1]]
			total = 0
			for j in range(1,5):
				total += int(line[j])
			vector[no] = total
	return vector

def JSD(P,Q):
	_P = np.array(P)
	_Q = np.array(Q)
	_M = 0.5 * (_P + _Q)
	return 0.5 * (entropy(_P, _M) + entropy(_Q, _M))

n = 934	
f = open("histogram_4cluster.csv","r")
file = csv.reader(f)
file_data = []
for line in file:
	if file.line_num == 1:
		continue
	file_data.append(line)
	
X = []
for i in range(0,n):
	a = data_filter(i+1)
	print(str(i)+": "+str(a))
	X.append(a)

Dist = np.empty([n,n])
for i in range(0,n):
	p = X[i]
	for j in range(0,n):
		q = X[j]
		Dist[i, j] = JSD(p, q)
print(Dist)	
f = open("distance_4cluster.json","w")
dict = {}
for i in range(0,n):
	tmp = []
	l = list(Dist[i])
	tmp.append(l.index(max(l))+1)
	tmp.append(max(l))
	tmp.append(l)
	dict[str(i+1)] = tmp
json.dump(dict,f)
	
