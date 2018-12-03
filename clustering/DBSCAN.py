from clustering.Clustering import Clustering
from copy import deepcopy

class DBSCAN(Clustering):

    DISTANCE_EUCLIDEAN = 'eucl'
    DISTANCE_MANHATTAN = 'manh'

    def __init__(self):
        self.dMatrix = []
        super().__init__()


    #######################################################
    # DBSCAN CLUSTERING
    #
    # data         = Dataset to be clustered (list containing dictionarys)
    # eps          = Radius of a 'neigbourhood'
    # MinPts       = Minimum amount of points required in eps-neighbourhood
    # dist         = Distance function (eucl=Euclidean | manh=Manhattan)
    # filterKeys   = keys to be filtered out before computing distances
    #
    # returns the same data set with one extra attribute namely 'cluster'
    #
    def cluster(self, data, eps=1, MinPts=4, dist=DISTANCE_EUCLIDEAN, filterKeys=[]):
        # Take deepcopy of the data (don't want to edit the original dataset)
        data = deepcopy(data)

        # Keys (i.e values) that are ignored in classification computations (distances etc.)
        self.filterKeys.extend(filterKeys)
        self.filterKeys.append(self.CLUSTER_KEY)

        for case in data:
            case[self.CLUSTER_KEY] = ''
        
        # This next 'code block' is mostly following the tutorial found from 
        # https://medium.com/nearist-ai/dbscan-clustering-tutorial-dd6a9b637a4b
        labels = [0]*len(data)
        clusterNum = 0
        for point in range(len(data)):
            if not (labels[point] == 0):
                continue
            neighbours = self.getNeighbours(data, point, eps, dist)
            if len(neighbours) < MinPts:
                labels[point] = -1
            else:
                clusterNum += 1
                labels[point] = clusterNum
                self.completeCluster(clusterNum, data, labels, point, eps, MinPts, dist)

        for i, case in enumerate(data):
            case[self.CLUSTER_KEY] = '%s%d' % (self.CLUSTER_NAME_PREFIX, labels[i])

        print("DBSCAN done!")
        return data


    # Assigning relevant cases (in data) into the cluster
    #
    # This method is mostly following the tutorial found from 
    # https://medium.com/nearist-ai/dbscan-clustering-tutorial-dd6a9b637a4b
    def completeCluster(self, clusterNum, data, labels, point, eps, MinPts, dist):
        searchQueue = [point]
        i = 0
        while i < len(searchQueue):
            point = searchQueue[i]
            neighbours = self.getNeighbours(data, point, eps, dist)
            if len(neighbours) < MinPts:
                i += 1
                continue
            for neighbour in neighbours:
                if labels[neighbour] == -1:
                    labels[neighbour] = clusterNum
                elif labels[neighbour] == 0:
                    labels[neighbour] = clusterNum
                    searchQueue.append(neighbour)
            i += 1


    # Getting the eps-neighbourhood points of a point
    #
    # This method is mostly following the tutorial found from 
    # https://medium.com/nearist-ai/dbscan-clustering-tutorial-dd6a9b637a4b
    def getNeighbours(self, data, point, eps, dist):
        n = []
        for p in range(len(data)):
            if self.distance(data[point], data[p], dist) <= eps:
                n.append(p)
        return n
