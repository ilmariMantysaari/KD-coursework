from clustering.Clustering import Clustering
from copy import deepcopy
import random

class kMeans(Clustering):

    DISTANCE_EUCLIDEAN = 'eucl'
    DISTANCE_MANHATTAN = 'manh'

    METHOD_RANDOM      = 'rand'
    METHOD_DISTANCE    = 'dist'
    CLUSTER_DISTANCE_KEY = 'dist2clu'

    def __init__(self):
        iterCentres = []    # Centre points for each cluster in every iteration round
        iterData = []       # Clustered data set in every iteration round
        super().__init__()


    #######################################################
    # K-MEANS CLUSTERING
    #
    # data         = Dataset to be clustered (list containing dictionarys)
    # k            = Number of clusters (integer)
    # dist         = Distance function (eucl=Euclidean | manh=Manhattan)
    # centreMethod = Method for selecting the cluster centres (rand=Random | dist=Distance (furthest))
    # filterKeys   = keys to be filtered out before computing distances
    #
    def cluster(self, data, k=3, dist=DISTANCE_EUCLIDEAN, centreMethod=METHOD_RANDOM, filterKeys=[]):
        if self.DEVMODE: print("\nK-MEANS CLUSTERING:")

        # Take deepcopy of the data (don't want to edit the original dataset)
        data = deepcopy(data)
        dataCollector = []
        centerCollector = []

        # Keys (i.e values) that are ignored in classification computations (distances etc.)
        self.filterKeys.extend(filterKeys)
        self.filterKeys.extend([self.CLUSTER_KEY, self.CLUSTER_DISTANCE_KEY])

        for i, case in enumerate(data):
            # Assigning each case into a cluster, which initially is itself
            case[self.CLUSTER_KEY] = "Case%d" % (i)
            case[self.CLUSTER_DISTANCE_KEY] = 0.0

            # TODO: Do this in preprocessing!
            # Turn attributes into floats:
            # for att in self.dictionaryWithoutKeys(case, self.filterKeys):
            #     case[att] = float(case[att])

        clusterCentres = self.selectClusterCentres(centreMethod, data, k)
        centerCollector.append(deepcopy(clusterCentres))

        while True:
            # Assign cluster for each case (if not any changes, break the loop)
            if self.assignClusterCentres(data, clusterCentres, dist):
                # Update cluster centres by computing the mean values for each attribute
                self.updateClusterCentres(clusterCentres, data)
                # Collect data and center points for each phase
                centerCollector.append(deepcopy(clusterCentres))
                dataCollector.append(deepcopy(data))
                if self.DEVMODE: print("\n   Updated cluster centroids -> New round with a loop...\n")
            else:
                dataCollector.append(deepcopy(data))
                if self.DEVMODE: print("\nNo changes, clustering job done! It took %d iterations after initial round." % (len(dataCollector)-1))
                break

        if self.DEVMODE: print()

        self.iterCentres = centerCollector
        self.iterData = dataCollector

        return data


    #######################################################
    # Selecting the k cluster centroids with a given method
    #
    def selectClusterCentres(self, method, data, k):
        c = []
        if method == self.METHOD_RANDOM:
            random.seed(12345) # Iris seems to work pretty well with seed 12345! (k=3, eucl)
            for i in range(k):
                c.append(dict( data[ random.randint(0, len(data)-1) ] ))
                # Remove unneccesary (for clusters) attributes
                for key in self.filterKeys:
                    c[i].pop(key, None)
                c[i][self.CLUSTER_KEY] = '%s%d' % (self.CLUSTER_NAME_PREFIX, i+1)
        elif method == self.METHOD_DISTANCE:
            # TODO ?:
            pass
        return c


    #######################################################
    # Assigns for each data point its closests cluster centre
    #
    def assignClusterCentres(self, data, clusterCentres, dist, ):
        changesMade = False
        for i, case in enumerate(data):
            distances = self.getDistances(case, clusterCentres, dist)
            closestsCluster = min(distances, key=distances.get)
            if case[self.CLUSTER_KEY] != closestsCluster:
                if self.DEVMODE: print("   UPDATE Case %d: (%s -> %s)" % (i, case[self.CLUSTER_KEY], closestsCluster))
                case[self.CLUSTER_KEY] = closestsCluster
                changesMade = True
            case[self.CLUSTER_DISTANCE_KEY] = distances[closestsCluster]
            if self.DEVMODE: print("   Case %d: %s (%s %.3f)" % (i, case[self.CLUSTER_KEY], self.CLUSTER_DISTANCE_KEY, case[self.CLUSTER_DISTANCE_KEY]))
            # if self.DEVMODE: print("   %d: %s" % (i, case))
        return changesMade


    #######################################################
    # Updates cluster centres
    # by computing the mean attribute values of cases in each cluster
    #
    def updateClusterCentres(self, clusters, data):
        for cluster in clusters:
            # Initialize every attribute into 0.
            for att in self.dictionaryWithoutKeys(cluster, self.filterKeys):
                cluster[att] = 0
            n = 0
            for case in data:
                if case[self.CLUSTER_KEY] == cluster[self.CLUSTER_KEY]:
                    # Add a value of each attribute of each case into a clusters corresponding attribute
                    for att in self.dictionaryWithoutKeys(case, self.filterKeys):
                        cluster[att] += case[att]
                    n += 1

            if n > 0:
                # Divide added/summed attribute values with n (number of cases in a cluster) to get the mean of the values
                for att in self.dictionaryWithoutKeys(cluster, self.filterKeys):
                    cluster[att] = cluster[att]/n
