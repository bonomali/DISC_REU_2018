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


network_file = "int-structure-classes.emb"

network_data = np.genfromtxt(network_file, delimiter=' ')

with open('nodes_classified.csv') as f:
    next(f)  # Skip the header
    reader = csv.reader(f, skipinitialspace=True)
    mod_class_dict = dict(reader)

with open('object_ref.csv') as f:
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
num_clusters = 10
cmap = plt.cm.jet
bounds = np.linspace(0,num_clusters,num_clusters+1)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

#label colors according to Gephi
mod_classes = []
for sequence in node_sequences:
	mod_class = int(mod_class_dict[str(sequence)])#[sequence])
	mod_classes.append(mod_class)

#or, define colors by k-means clusters
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
for index in range(len(node_sequences)):
	sequence = list(node_sequences)[index]
	gephi = mod_classes[index]
	Kmeans_15D = labels[index]
	Kmeans_2D = labls[index]
	line_dict = {'sequence':str(sequence), 'Gephi':str(gephi), 'KMeans_15D': str(Kmeans_15D), 'KMeans_2D' : str(Kmeans_2D)}
	csv_data.append(line_dict)

with open("struc2vec-classified.csv",'w') as resultFile:
	fieldnames = ['sequence', 'Gephi', 'KMeans_15D', 'KMeans_2D']
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
