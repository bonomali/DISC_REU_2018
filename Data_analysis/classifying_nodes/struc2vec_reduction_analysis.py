"""
This script makes use of the Node2Vec python implementation (included in the node2vec package that can be installed as usual with pip3).
Node2Vec is used to generate embeddings (vectors) in high-dimensional space, which are then used to classify nodes as being in different groups, usign KMeans clustering on both the original (high-dimensinoal) embeddings data *and* using TSNE to visualise data in a 2-D space.
Furthermore, we also use struc2vec to generate the structural identity of each node.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import csv
import numpy as np

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from node2vec import Node2Vec
from sklearn.cluster import KMeans

import replace_sequence_str_int as str_to_int
import main
import sys

from os import listdir
from os.path import isfile, join

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
	
	#Define colors by k-means clusters
	estimator = KMeans(n_clusters = num_clusters)
	estimator.fit(node_vectors)
	labels = estimator.labels_
	
	
	#Apply T-SNE to visualise
	tsne = TSNE(n_components=2, verbose=1, perplexity=8, early_exaggeration=3, n_iter=1000)
	tsne_results = tsne.fit_transform(node_vectors)
	
	tsne_one = tsne_results[:,0]
	tsne_two = tsne_results[:,1]
	
	#Then apply the same KMeans to 2-D data
	est = KMeans(n_clusters = num_clusters)
	est.fit(tsne_results)
	labls = est.labels_
	
	#Plot T-SNE results
	fig, axes = plt.subplots(1,2, figsize=(5,3.5))
	scat = axes[0].scatter(tsne_one,tsne_two,c=labels,cmap=cmap, norm=norm)
	axes[0].set_title("KMeans applied first, then T-SNE")
	scat = axes[1].scatter(tsne_one, tsne_two, c=labls, cmap=cmap, norm=norm)
	axes[1].set_title("T-SNE applied first, then KMeans")
	
	ax2 = fig.add_axes([0.9, 0.1, 0.03, 0.8])
	cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')
	
	csv_data = []
	for index in range(len(node_sequences)):
		sequence = list(node_sequences)[index]
		Kmeans_15D = labels[index]
		Kmeans_2D = labls[index]
		line_dict = {'sequence':str(sequence), 'struc2vec128D': str(Kmeans_15D), 'struc2vec2D' : str(Kmeans_2D)}
		csv_data.append(line_dict)
	
	return(csv_data)





def node2vec_gen(HON_file = "",
				 outfile = "node2vec-directed-classified",
				 p=1.0, q=1.0,
				 num_clusters = 12):
	
	network_data = nx.read_weighted_edgelist(HON_file, nodetype=str)

	weights=[]
	G = nx.DiGraph()
	for line in network_data.edges(data=True):
		print(line)
		left_node = line[0]
		right_node = line[1]
		weight = float(line[2]["weight"])
		weights.append(weight)
		G.add_edge(left_node, right_node, weight= weight)	
	
	#Define stuff for colorbar
	cmap = plt.cm.jet
	bounds = np.linspace(0,num_clusters,num_clusters+1)
	norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	
	# Generate walks
	node2vec = Node2Vec(G, dimensions=15, walk_length=30, num_walks=100, p=p, q=q)
	# Learn embeddings 
	model = node2vec.fit(window=20, min_count=1)
	
	vectors = model[model.wv.vocab]
	sequences = model.wv.vocab.keys()
	
	#or, define colors by k-means clusters
	estimator = KMeans(n_clusters = num_clusters)
	estimator.fit(vectors)
	labels = estimator.labels_
	
	
	#Apply T-SNE to visualise
	tsne = TSNE(n_components=2, verbose=1, perplexity=8, early_exaggeration=3, n_iter=1000)
	tsne_results = tsne.fit_transform(vectors)
	
	tsne_one = tsne_results[:,0]
	tsne_two = tsne_results[:,1]
	
	#Then apply the same KMeans to 2-D data
	est = KMeans(n_clusters = num_clusters)
	est.fit(tsne_results)
	labls = est.labels_
	
	#Plot T-SNE results
	fig, axes = plt.subplots(1,2, figsize=(5,3.5))
	scat = axes[0].scatter(tsne_one,tsne_two,c=labels,cmap=cmap, norm=norm)
	axes[0].set_title("KMeans applied to 128-D data")
	scat = axes[1].scatter(tsne_one, tsne_two, c=labls, cmap=cmap, norm=norm)
	axes[1].set_title("KMeans applied to 2D TSNE data")
	
	ax2 = fig.add_axes([0.9, 0.1, 0.03, 0.8])
	cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')	
	
	csv_data = []
	for index in range(len(sequences)):
		sequence = list(sequences)[index]
		Kmeans_15D = labels[index]
		Kmeans_2D = labls[index]
		line_dict = {'sequence':str(sequence), 'node2vec128D': str(Kmeans_15D), 'node2vec2D' : str(Kmeans_2D)}
		csv_data.append(line_dict)
	
	return(csv_data)



def classifying(MinSupport = 10, MaxOrder = 99, num_clusters = 10, p=1.0, q=1.0, num_communities = 14,
				HON_file = "weighted-network-all.edge",out = "struc2vec-directed-classified"):
	node2vec_data = node2vec_gen(HON_file = HON_file, num_clusters = num_communities, p=p, q=q)
	struc2vec_data = struc2vec_gen(HON_file=HON_file, MinSupport=MinSupport, MaxOrder=MaxOrder, num_clusters=num_clusters)
	
	full_dicts = []
	for index in range(len(struc2vec_data)):
		sequence = struc2vec_data[index]["sequence"]
		node2vec128D = node2vec_data[index]["node2vec128D"]
		node2vec2D = node2vec_data[index]["node2vec2D"]
		struc2vec128D = struc2vec_data[index]["struc2vec128D"]
		struc2vec2D = struc2vec_data[index]["struc2vec2D"]
		full_dict = {'sequence':str(sequence), "node2vec128D":node2vec128D, "node2vec2D":node2vec2D,"struc2vec128D":struc2vec128D,"struc2vec2D":struc2vec2D}
		full_dicts.append(full_dict)
	
	out_file = out + str(MaxOrder) + ".csv"
	
	with open(out_file,'w') as resultFile:
		fieldnames = ['sequence', 'struc2vec128D', 'struc2vec2D', 'node2vec128D', 'node2vec2D']
		writer = csv.DictWriter(resultFile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(full_dicts)	





	
##  Combine all sub-HON graphs into a single HON graph
sequence_path = "../Neural_Net/HON_Files"
network_files = [f for f in listdir(sequence_path) if isfile(join(sequence_path, f))]

network_data = np.genfromtxt(sequence_path+"/"+network_files[0], delimiter=',',dtype=('U100', 'U100', float), skip_header = 1)	
weights=[]
G = nx.DiGraph()
for line in network_data:
	left_node = line[0]
	right_node = line[1]
	weight = float(line[2])
	weights.append(weight)
	G.add_edge(left_node, right_node, weight= weight)


for index in range(1,len(network_files)):
	network = network_files[index]
	network_data = np.genfromtxt(sequence_path+"/"+network, delimiter=',',dtype=('U100', 'U100', float), skip_header = 1)
	
	weights=[]
	H = nx.DiGraph()
	for line in network_data:
		left_node = line[0]
		right_node = line[1]
		weight = float(line[2])
		weights.append(weight)
		H.add_edge(left_node, right_node, weight= weight)	
	G = nx.compose(H, G)

nx.write_weighted_edgelist(G, "weighted-network-all.edge")

classifying()

plt.show()
