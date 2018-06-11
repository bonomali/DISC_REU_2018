import plotly.plotly as py
import plotly.graph_objs as go

import matplotlib.pyplot as plt

import networkx as nx
import csv
import numpy as np


network_file = "weights-network-cell.csv"
network_file = "network-cell.csv"

network_data = np.genfromtxt(network_file, delimiter=',',dtype=None)[:20]

nodes = []
weights = []
for line in network_data:
	left_node = line[0]
	right_node = line[1]
	weight = line[2]
	nodes.append((left_node, right_node))
	weights.append(weight)


G = nx.DiGraph()
G.add_edges_from(nodes)

pos=nx.spring_layout(G)

colors = np.array(weights)
cmap = plt.get_cmap('hsv')
vmin = min(colors)
vmax = max(colors)
nx.draw(G, pos, node_color='grey', edge_color=colors, width=2, edge_cmap=cmap,
					   node_size=10, with_labels=False, font_size=8, vmin=vmin, vmax=vmax)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
sm._A = []

plt.colorbar(sm)
for key in pos.keys():
	x,y = pos[key]
	plt.text(x,y+0.1,s=key, fontsize=6, bbox=dict(facecolor='red', alpha=0.5),horizontalalignment='center')

plt.show()

