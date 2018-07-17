import numpy as np
import matplotlib.pyplot as plt
import csv

data = np.genfromtxt("network-cell-99MinSupport-1.csv", delimiter = ',',dtype=('U100','U100', float), skip_header=1)
objects = []
for line in data:
	freq = line[2]
	objects.append(freq)

np_data = np.asarray(objects)

bins = []
for i in range(0,100):
	bins.append(i)

n, bins, patches = plt.hist(np_data, bins=bins, color='green')

bin_centers = 0.5 * (bins[:-1] + bins[1:])

col = bin_centers - min(bin_centers)
col /= max(col)
cm = plt.cm.get_cmap('Spectral')

for c, p in zip(col, patches):
	plt.setp(p, 'facecolor', cm(c))

plt.figure()
plt.bar(bins[0:99], 100*n/sum(n))
