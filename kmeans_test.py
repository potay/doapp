import random, pprint
import matplotlib.pyplot as plt
import sklearn.cluster
import numpy as np

dataset = []

groups = 3
sampleSize = 1000

color = ['r+', 'b+', 'g+']

minM, maxM = 0, 100
minU, maxU = 1, 5

for i in xrange(groups-1):
    groupSize = random.randint(10, sampleSize)
    sampleSize -= groupSize
    xm, ym = random.randint(minM,maxM), random.randint(minM,maxM)
    xu, yu = random.randint(minU,maxU), random.randint(minU,maxU)
    for j in xrange(groupSize):
        x, y = (random.normalvariate(xm, xu), random.normalvariate(ym, yu))
        dataset += [(x,y)]
        plt.plot([x],[y],color[i])

xm, ym = random.randint(minM,maxM), random.randint(minM,maxM)
xu, yu = random.randint(minU,maxU), random.randint(minU,maxU)

for j in xrange(sampleSize):
    x, y = (random.normalvariate(xm, xu), random.normalvariate(ym, yu))
    dataset += [(x,y)]
    plt.plot([x],[y],color[groups-1])

print "done"

plt.show()

dataset = np.array(dataset)
k = 3
cList = []

learn = sklearn.cluster.KMeans(n_clusters=k, init='k-means++', n_init=10, max_iter=300, tol=0.0001, precompute_distances=True, verbose=0, random_state=None,
                       #copy_x=True,
                       n_jobs=-1)

result = learn.fit_predict(dataset)

color = ['ro', 'bo', 'go', 'r+', 'b+', 'g+', 'rx', 'bx', 'gx']

for i in xrange(len(result)):
    plt.plot(dataset[i][0], dataset[i][1], color[result[i]])


plt.show()

learn = sklearn.cluster.DBSCAN(eps=0.5, min_samples=5, metric='euclidean', algorithm='auto', leaf_size=30, p=None, random_state=None)

result = learn.fit_predict(dataset)
pprint.pprint(result)

color = ['ro', 'bo', 'go', 'r+', 'b+', 'g+', 'rx', 'bx', 'gx']

for i in xrange(len(result)):
    plt.plot(dataset[i][0], dataset[i][1], color[result[i]])


plt.show()
