"""
This script makes use of the Node2Vec python implementation (included in the node2vec package that can be installed as usual with pip3).
Node2Vec is used to generate embeddings (vectors) in high-dimensional space, which are then used to classify nodes as being in different groups, usign KMeans clustering on both the original (high-dimensinoal) embeddings data *and* using TSNE to visualise data in a 2-D space.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import csv
import numpy as np

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from node2vec import Node2Vec
from sklearn.cluster import KMeans

def node2vec_gen(network_file = "../HON_Creation/network-cell-1storder-weights.csv",
				 gephi_classifications_file = "../Gephi_files/network-1st-order.csv",
				 node2vec_classifications_file = "node2vec-1st-order-classes.csv",
				 p=1.0, q=1.0):
	
	network_data = np.genfromtxt(network_file, delimiter=',',dtype=('U100', 'U100', float), skip_header = 1)
	
	weights=[]
	G = nx.DiGraph()
	for line in network_data:
		left_node = line[0]
		right_node = line[1]
		weight = float(line[2])
		weights.append(weight)
		G.add_edge(left_node, right_node, weight= weight)
	
	nx.write_gexf(G, "weighted-network-all.gexf")
	
	with open(gephi_classifications_file) as f:
	    next(f)  # Skip the header
	    reader = csv.reader(f, skipinitialspace=True)
	    mod_class_dict = dict(reader)
	
	number_of_classes = len(set(mod_class_dict.values()))
	
	
	#Define stuff for colorbar
	cmap = plt.cm.jet
	bounds = np.linspace(0,number_of_classes,number_of_classes+1)
	norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
	
	# Generate walks
	node2vec = Node2Vec(G, dimensions=15, walk_length=30, num_walks=100, p=p, q=q)
	# Learn embeddings 
	model = node2vec.fit(window=20, min_count=1)
	
	vectors = model[model.wv.vocab]
	sequences = model.wv.vocab.keys()
	mod_classes = []
	
	#label colors
	for sequence in sequences:
		mod_class = int(mod_class_dict[str(sequence)])#[sequence])
		mod_classes.append(mod_class)
	
	#or, define colors by k-means clusters
	estimator = KMeans(n_clusters = number_of_classes)
	estimator.fit(vectors)
	labels = estimator.labels_
	
	
	#Apply T-SNE to visualise
	tsne = TSNE(n_components=2, verbose=1, perplexity=8, early_exaggeration=3, n_iter=1000)
	tsne_results = tsne.fit_transform(vectors)
	
	tsne_one = tsne_results[:,0]
	tsne_two = tsne_results[:,1]
	
	#Then apply the same KMeans to 2-D data
	est = KMeans(n_clusters = number_of_classes)
	est.fit(tsne_results)
	labls = est.labels_
	
	#Plot T-SNE results
	fig, axes = plt.subplots(1,3, figsize=(5,3.5))
	scat = axes[0].scatter(tsne_one,tsne_two,c=mod_classes,cmap=cmap, norm=norm)
	axes[0].set_title("Gephi classes")
	scat = axes[1].scatter(tsne_one,tsne_two,c=labels,cmap=cmap, norm=norm)
	axes[1].set_title("KMeans applied to 15-D data")
	scat = axes[2].scatter(tsne_one, tsne_two, c=labls, cmap=cmap, norm=norm)
	axes[2].set_title("KMeans applied to 2D TSNE data")
	
	ax2 = fig.add_axes([0.9, 0.1, 0.03, 0.8])
	cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')	
	
	csv_data = []
	for index in range(len(sequences)):
		sequence = list(sequences)[index]
		gephi = mod_classes[index]
		Kmeans_15D = labels[index]
		Kmeans_2D = labls[index]
		line_dict = {'sequence':str(sequence), 'Gephi':str(gephi), 'KMeans_15D': str(Kmeans_15D), 'KMeans_2D' : str(Kmeans_2D)}
		csv_data.append(line_dict)
	
	with open(node2vec_classifications_file,'w') as resultFile:
		fieldnames = ['sequence', 'Gephi', 'KMeans_15D', 'KMeans_2D']
		writer = csv.DictWriter(resultFile, fieldnames=fieldnames)
		writer.writeheader()
		writer.writerows(csv_data)
	

node2vec_gen(network_file = "../HON_Creation/network-cell-1storder-weights.csv",
				 gephi_classifications_file = "../Gephi_files/network-1st-order.csv",
				 node2vec_classifications_file = "node2vec-1st-order-classes.csv")

node2vec_gen(network_file = "../HON_Creation/network-cell-2ndorder-weights.csv",
				 gephi_classifications_file = "../Gephi_files/network-2nd-order.csv",
				 node2vec_classifications_file = "node2vec-2nd-order-classes.csv")

node2vec_gen(network_file = "../HON_Creation/network-cell-3rdorder-weights.csv",
				 gephi_classifications_file = "../Gephi_files/network-3rd-order.csv",
				 node2vec_classifications_file = "node2vec-3rd-order-classes.csv")

node2vec_gen(network_file = "../HON_Creation/network-cell-4thorder-weights.csv",
				 gephi_classifications_file = "../Gephi_files/network-4th-order.csv",
				 node2vec_classifications_file = "node2vec-4th-order-classes.csv")

node2vec_gen(network_file = "../HON_Creation/network-cell-5thorder-weights.csv",
				 gephi_classifications_file = "../Gephi_files/network-5th-order.csv",
				 node2vec_classifications_file = "node2vec-5th-order-classes.csv")
plt.show()

