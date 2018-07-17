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

def struc2vec_gen(HON_dir = "../HON_Creation/", 
				  reference = "object-ref_order", 
				  int_file = 'int-network-cell_order',
				  out_embeddings_file = "int-structure-classes",
				  MinSupport = 8, MaxOrder = 99, out_file_add = '',
				  out = "struc2vec-directed-classified",
				  num_clusters = 4):
	
	#  First, generate files that use integers for each node instead of string sequences
	str_to_int.replace_sequence_str_int(HON_dir = HON_dir, reference = reference, int_file = int_file, MinSupport=MinSupport, MaxOrder=MaxOrder, out_file_add='')
	
	out_embeddings_file = "int-structure-classes" + str(MaxOrder) + ".txt"
	out_file = out + str(MaxOrder) + ".csv"
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
	
	#  Sort out gephi classifications so that the force-directed graph will work still.
	#with open(gephi_file) as f:
	#	next(f)  # Skip the header
	#	reader = csv.reader(f, skipinitialspace=True)
	#	mod_class_dict = dict(reader)
	#mod_classes = []
	#for sequence in node_sequences:
	#	mod_class = int(mod_class_dict[str(sequence)])#[sequence])
	#	mod_classes.append(mod_class)
	
	#Define stuff for colorbar
	num_clusters = 4
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
	axes[0].set_title("KMeans applied to 128-D data")
	scat = axes[1].scatter(tsne_one, tsne_two, c=labls, cmap=cmap, norm=norm)
	axes[1].set_title("KMeans applied to 2D TSNE data")
	
	ax2 = fig.add_axes([0.9, 0.1, 0.03, 0.8])
	cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')
	
	csv_data = []
	for index in range(len(node_sequences)):
		sequence = list(node_sequences)[index]
		#gephi = mod_classes[index]
		gephi = 1
		Kmeans_15D = labels[index]
		Kmeans_2D = labls[index]
		line_dict = {'sequence':str(sequence), 'Gephi':str(gephi), 'KMeans_15D': str(Kmeans_15D), 'KMeans_2D' : str(Kmeans_2D)}
		csv_data.append(line_dict)
	
	with open(out_file,'w') as resultFile:
		fieldnames = ['sequence', 'Gephi', 'KMeans_15D', 'KMeans_2D']
		writer = csv.DictWriter(resultFile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(csv_data)	

#struc2vec_gen(MinSupport = 8, MaxOrder = 1)
#struc2vec_gen(MinSupport = 8, MaxOrder = 2)
struc2vec_gen(MinSupport = 8, MaxOrder = 3)
#struc2vec_gen(MinSupport = 8, MaxOrder = 4)
#struc2vec_gen(MinSupport = 8, MaxOrder = 5)
#struc2vec_gen(MinSupport = 8, MaxOrder = 6)
#struc2vec_gen(MinSupport = 8, MaxOrder = 7)
#struc2vec_gen(MinSupport = 8, MaxOrder = 8)
#struc2vec_gen(MinSupport = 8, MaxOrder = 9)

plt.show()
