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


network_file = "weights-network-cell.csv"

network_data = np.genfromtxt(network_file, delimiter=',',dtype=('U100', 'U100', float))

weights=[]
G = nx.DiGraph()
for line in network_data:
	left_node = line[0]
	right_node = line[1]
	weight = float(line[2])
	weights.append(weight)
	G.add_edge(left_node, right_node, weight= weight)

nx.write_gexf(G, "weighted-network-all.gexf")
with open('nodes_classified.csv') as f:
    next(f)  # Skip the header
    reader = csv.reader(f, skipinitialspace=True)
    mod_class_dict = dict(reader)



#Define stuff for colorbar
cmap = plt.cm.jet
bounds = np.linspace(0,16,16)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# Generate walks
node2vec = Node2Vec(G, dimensions=15, walk_length=30, num_walks=100)
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
estimator = KMeans(n_clusters = 16)
estimator.fit(vectors)
labels = estimator.labels_


#Apply T-SNE to visualise
tsne = TSNE(n_components=2, verbose=1, perplexity=8, early_exaggeration=3, n_iter=1000)
tsne_results = tsne.fit_transform(vectors)

tsne_one = tsne_results[:,0]
tsne_two = tsne_results[:,1]

#Then apply the same KMeans to 2-D data
est = KMeans(n_clusters = 16)
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
	line_dict = {'sequence':str(sequence), 'Gephi':str(gephi), '15D_KMeans': str(Kmeans_15D), '2D_KMeans' : str(Kmeans_2D)}
	csv_data.append(line_dict)

with open("nodes_doubly_classified.csv",'w') as resultFile:
	fieldnames = ['sequence', 'Gephi', '15D_KMeans', '2D_KMeans']
	writer = csv.DictWriter(resultFile, fieldnames=fieldnames)
	writer.writeheader()
	writer.writerows(csv_data)











##Ok, so, PCA, T-SNE, Isomap... aren't working very well... PCA only conserves ~8% of variation in 3 dimensions, and T-SNE doesn't indicate any obvious clustering.
##Investigate alternative scikit-learn clustering algorithms, that don't require dimensional reduction first.
"""from sklearn.cluster import AffinityPropagation
from sklearn import metrics

af = AffinityPropagation(preference=-50).fit(vectors)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_

n_clusters_ = len(cluster_centers_indices)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels, metric='sqeuclidean'))
##This does not work -- cluster_centers_indices is "None" for some reason...
"""
