"""
This script makes use of the Node2Vec python implementation (included in the node2vec package that can be installed as usual with pip3).
Node2Vec is used to generate embeddings (vectors) in high-dimensional space, which are then used to classify nodes as being in different groups, usign KMeans clustering on both the original (high-dimensinoal) embeddings data *and* using TSNE to visualise data in a 2-D space.
Furthermore, we also use struc2vec to generate the structural identity of each node.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import csv
import numpy as np

from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

import replace_sequence_str_int as str_to_int
import main
import sys
sys.path.append("../HON_Creation/")

from os import listdir
from os.path import isfile, join
from jianxu_main import fast_build_HON


### Function to generate struc2vec vectors
def struc2vec_gen(HON_file = "",
				  reference = "object-ref_order", 
				  int_file = 'int-network-cell_order',
				  out_embeddings_file = "int-structure-classes",
				  MinSupport = 10, MaxOrder = 99, out_file_add = '',
				  num_clusters = 4):
	
	#  First, generate files that use integers for each node instead of string sequences
	str_to_int.replace_sequence_str_int(HON_file = HON_file, reference = reference, int_file = int_file, MinSupport=MinSupport, MaxOrder=MaxOrder, out_file_add='')
	
	out_embeddings_file = "int-structure-classes" + str(MaxOrder) + ".txt"
	int_file = int_file + str(MaxOrder) + ".csv"
	reference_csv = reference + str(MaxOrder) + ".csv"
	
	#  Then, using these files, 
	main.run_remote(int_file, out_embeddings_file)
	 
	network_data = np.genfromtxt(out_embeddings_file, delimiter=' ', skip_header=1)
	
	with open(reference_csv) as f:
	    reader = csv.reader(f)
	    object_ref = dict(reader)
	
	#Ok, now need to reverse the dictionary, st the keys correspond to numbers and the sequence is the value
	
	sequence_ref = {}
	for key in object_ref.keys():
		sequence_ref[object_ref[key]] = key
	
	#Create two lists: One that contains node sequences (e.g. "36|18", etc), and one that contains the struc2vec vectors.
	node_sequences = []
	node_vectors = []
	for line in network_data:
		node = line[0]
		vector = line[1:]
		node_seq = sequence_ref[str(int(node))]
		node_sequences.append(node_seq)
		node_vectors.append(vector)
	
	
	#Define stuff for colorbar
	cmap = plt.cm.jet
	bounds = np.linspace(0,num_clusters,num_clusters+1)
	norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	
	#Define classes by k-means clusters
	estimator = KMeans(n_clusters = num_clusters)
	estimator.fit(node_vectors)
	labels = estimator.labels_
		
	csv_data = []
	for index in range(len(node_sequences)):
		sequence = list(node_sequences)[index]
		Kmeans = labels[index]
		line_dict = {'sequence':str(sequence), 'struc2vec128D': str(Kmeans)}
		csv_data.append(line_dict)
	
	return(csv_data)



###  Load up the gephi community classifications.
def community_gen(gephi_file = "modularity_classes.csv"):
	modularity_classes = {}
	fieldnames = ['Id','modularity_class']
	in_file = open(gephi_file)
	reader = csv.DictReader(in_file, fieldnames=fieldnames)
	next(reader, None)
	for row in reader:
		modularity_classes[row["Id"]] = row["modularity_class"]
	return modularity_classes



###  Runs community_gen and struc2vec_gen
def classifying(MinSupport=10, MaxOrder=99, num_clusters=4,
				HON_file="weighted-network-all.csv", out="fdd_nodes_all", gephi_file="modularity_classes.csv"):
	community_data = community_gen(gephi_file=gephi_file)
	struc2vec_data = struc2vec_gen(HON_file=HON_file, MinSupport=MinSupport, MaxOrder=MaxOrder, num_clusters=num_clusters)
	
	full_dicts = []
	for index in range(len(struc2vec_data)):
		sequence = struc2vec_data[index]["sequence"]
		community = community_data[struc2vec_data[index]["sequence"]]
		struc2vec128D = struc2vec_data[index]["struc2vec128D"]
		full_dict = {'sequence':str(sequence), "community":community, "struc2vec128D":struc2vec128D}
		full_dicts.append(full_dict)
	
	out_file = out + str(MaxOrder) + ".csv"
	
	with open(out_file,'w') as resultFile:
		fieldnames = ['sequence', 'struc2vec128D', 'community']
		writer = csv.DictWriter(resultFile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(full_dicts)	





	
##  Combine all sub-HON graphs into a single HON graph
sequence_path = "../../Raw_data_processing_JSON_to_CSV/Sequence_Data/sequenceAll_no100_clicks.txt"
output = "HON_all_no100.csv"
fast_build_HON(MinSupport = 50, MaxOrder= 6, Freq = False, Input_Sequence_File=sequence_path, OutputNetworkFile=output)

network_data = np.genfromtxt(output, delimiter=',',dtype=('U100', 'U100', float), skip_header = 1)	
weights=[]
G = nx.DiGraph()
for line in network_data:
	left_node = line[0]
	right_node = line[1]
	weight = float(line[2])
	weights.append(weight)
	G.add_edge(left_node, right_node, weight= weight)


nx.write_weighted_edgelist(G, "weighted-network-all.csv")

classifying(MinSupport = 50, MaxOrder= 6)

plt.show()
