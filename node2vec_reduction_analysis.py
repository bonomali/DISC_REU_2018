import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import csv
import numpy as np

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

#First, load in the modularity classes dictionary
with open('nodes_classified_8groups.csv') as f:
    next(f)  # Skip the header
    reader = csv.reader(f, skipinitialspace=True)
    mod_class_dict = dict(reader)
    print(mod_class_dict)


#Then load in node2vec vectors, separating sequence labels from vectors
node2vec_vectors = np.genfromtxt("node2vec-vectors.csv", dtype=None, delimiter=" ", skip_header=1)

mod_classes = []
vectors = []

for vector in node2vec_vectors:
	sequence = list(vector)[0].decode("utf-8")
	mod_class = int(mod_class_dict[sequence])
	mod_classes.append(mod_class)
	vectors.append(list(vector)[1:])
	#vectors_dict[sequence.decode("utf-8")] = dimensions

vectors = np.asarray(vectors)

'''Principal Component Analysis '''
cmap = plt.cm.jet
bounds = np.linspace(0,7, 8)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)


pca = PCA(n_components=32)
pca_result = pca.fit_transform(vectors)
print('Cumulative explained variation for 32 principal components: {}'.format(np.sum(pca.explained_variance_ratio_)))


pca_2 = PCA(n_components=2)
pca_2_result = pca_2.fit_transform(vectors)

print('Cumulative explained variation for 2 principal components: {}'.format(np.sum(pca.explained_variance_ratio_)))
figa, axa = plt.subplots(1,1, figsize=(6,6))
scat = axa.scatter(pca_2_result[:,0], pca_2_result[:,1], c=mod_classes, cmap=cmap, norm=norm)
ax2a = figa.add_axes([0.9, 0.1, 0.03, 0.8])
cb = mpl.colorbar.ColorbarBase(ax2a, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')
#ax = Axes3D(plt.gcf())
#ax.scatter(pca_one, pca_two, zs=pca_three)#, c=y, cmap = plt.cm.Spectral)


for n in range(1,10):
	tsne = TSNE(n_components=2, verbose=1, perplexity=n*10, early_exaggeration=10, n_iter=1000)
	tsne_results = tsne.fit_transform(pca_result)
	
	tsne_one = tsne_results[:,0]
	tsne_two = tsne_results[:,1]
	#tsne_three = tsne_results[:,2]
	fig, ax = plt.subplots(1,1, figsize=(6,6))
	scat = ax.scatter(tsne_one,tsne_two,c=mod_classes,cmap=cmap, norm=norm)
	plt.title("TSNE with perplexity =" + str(n*10))

	ax2 = fig.add_axes([0.9, 0.1, 0.03, 0.8])
	cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')





## Right, let's try a different dimensional reduction routine.
from sklearn.manifold import Isomap
#Isomap is from same clss as TSNE
for n in range(1,10):
	iso = Isomap(n_neighbors=n+1, n_components=2, eigen_solver='auto', tol=0, max_iter=None, path_method='auto', neighbors_algorithm='auto', n_jobs=1)
	iso_results = iso.fit_transform(vectors)
	
	iso_one = iso_results[:,0]
	iso_two = iso_results[:,1]
	
	error = iso.reconstruction_error() 
	
	fig, ax = plt.subplots(1,1, figsize=(6,6))
	scat = ax.scatter(iso_one,iso_two,c=mod_classes,cmap=cmap, norm=norm)
	plt.title("Isomap with n_neighbours =" + str(n))

	ax2 = fig.add_axes([0.9, 0.1, 0.03, 0.8])
	cb = mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds, format='%1i')





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
