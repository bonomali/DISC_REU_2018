
import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx
import csv
import numpy as np

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from node2vec import Node2Vec
from sklearn.cluster import KMeans


	

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

