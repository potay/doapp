import random, pprint
import matplotlib.pyplot as plt

dataset = []

groups = 3
sampleSize = 1000

color = ['r+', 'b+', 'g+']

for i in xrange(groups-1):
    groupSize = random.randint(10, sampleSize)
    sampleSize -= groupSize
    xm, ym = random.randint(0,100), random.randint(0,100)
    xu, yu = random.randint(10,20), random.randint(10,20)
    for j in xrange(groupSize):
        x, y = (random.normalvariate(xm, xu), random.normalvariate(ym, yu))
        dataset += [(x,y)]
        plt.plot([x],[y],color[i])

xm, ym = random.randint(0,100), random.randint(0,100)
xu, yu = random.randint(10,20), random.randint(10,20)

for j in xrange(sampleSize):
    x, y = (random.normalvariate(xm, xu), random.normalvariate(ym, yu))
    dataset += [(x,y)]
    plt.plot([x],[y],color[groups-1])

#pprint.pprint(dataset)

print "done"

import numpy as np
import matplotlib.pyplot as plt

#x = np.arange(0, 5, 0.1);
#y = np.sin(x)
#plt.plot(x, y)

#plt.plot(dataset, 'ro')
plt.show()

k = 3
cList = []

def getDistSquared(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (x1-x2)**2 + (y1-y2)**2

def getMin(l):
    currMin = None
    currMinDist = 99999999999999
    for t in l:
        if t[1] < currMinDist:
            currMinDist = t[1]
            currMin = t
    return currMin

def centerChangeSquared(c):
    addup = 0
    for point in c:
        if c[point][0] == (None, None):
            addup += 99999999999999
        else:
            addup += getDistSquared(point, c[point][0])
    return addup

def getClusterMean(l):
    X, Y = tuple(zip(*l))
    x = sum(X)/float(len(X))
    y = sum(Y)/float(len(Y))
    return (x, y)

def getBestClustering(cList):
    minChangeRating = 9999999999999.0
    minC = None
    for cTuple in cList:
        if cTuple[0] < minChangeRating:
            minChangeRating = cTuple[0]
            minC = cTuple[1]
    return minC

trials = 100

for i in xrange(trials):
    c = {}

    for i in xrange(k):
        point = random.choice(dataset)
        while point in c:
            point = random.choice(dataset)
        c[point] = [(None, None), []]

    epsilon = 1.0
    changeRating = None

    while True:
        for i in xrange(len(dataset)):
            cDistSquareds = []
            for point in c:
                c[point][0] = point
                cDistSquareds += [(point, getDistSquared(point, dataset[i]))]
            minSet = getMin(cDistSquareds)
            c[minSet[0]][1] += [dataset[i]]

        newC = {}
        for point in c:
            if len(c[point][1]) > 0:
                newPoint = getClusterMean(c[point][1])
            else:
                newPoint = (random.randint(0, 100), random.randint(0, 100))
            newC[newPoint] = [point, []]

        changeRating = centerChangeSquared(newC)
        if (changeRating > epsilon):
            c = newC
        else:
            break

    cList += [(changeRating, c)]

finalC = getBestClustering(cList)

#pprint.pprint(finalC)

color = ['ro', 'bo', 'go', 'r+', 'b+', 'g+', 'rx', 'bx', 'gx']

j = 0

for (point, value) in finalC.items():
    l = zip(*value[1])
    plt.plot(l[0], l[1], color[j])
    j += 1

#plt.plot([(10,10),(20,20),(30,30)], 'ro')
plt.show()
