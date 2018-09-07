import csv
f=open("object_ref.csv","r")
data = csv.reader(f)
f2 = open("object_ref_v3.csv","w")
f2.write("url,num,type\n")
for line in data:
	if line[0]!="Coursework":
		url = line[0].split('/')[-1][:-5]
	else:
		url = "Coursework"
	dict = eval(line[1])
	value = dict["ref_num"]
	type = dict["activity_type"]
	f2.write(url+','+value+','+type+'\n')