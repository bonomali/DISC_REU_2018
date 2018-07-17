# Node2Vec embedding, Community clustering, 
This script makes use of the Node2Vec python implementation (included in the node2vec package that can be installed as usual with pip3).
Node2Vec is used to generate embeddings (vectors) in high-dimensional space, which are then used to classify nodes as being in different groups, usign KMeans clustering on both the original (high-dimensinoal) embeddings data *and* using TSNE to visualise data in a 2-D space.

### Prerequisites

matplotlib, sklearn, node2vec, numpy, networkx. All modules can be installed by pip3.

Note that if you would like to modify the gephi_classifications_file (which defaults to files included in this Git repository), you will need to install the Gephi software and run the modularity classification on the appropriate dataset.

### How to Use

Open up node2vec_reduction_analysis.py in a text editor (e.g. gedit, vim). 

Change network_file, gephi_classifications_file, and node2vec_file, if necessary. If you'd like to use defaults, go to the order you're interested in (1st-5th, i.e. whether HON includes 1st-5th order sequences or not) and uncomment it, while commenting out all others.

```
network_file = "../HON_Creation/network-cell-1storder-weights.csv"
gephi_classifications_file = "../Gephi_files/network-1st-order.csv"
node2vec_classifications_file = "node2vec-1st-order-classes.csv"
```

Run the script in the command line.
