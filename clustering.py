from copy import deepcopy
import random

class Clustering():

    CLUSTER_KEY          = 'cluster'
    CLUSTER_NAME_PREFIX  = 'CLUSTER'
    CLUSTER_DISTANCE_KEY = 'dist2clu'

    DISTANCE_EUCLIDEAN = 'eucl'
    DISTANCE_MANHATTAN = 'manh'
    METHOD_RANDOM      = 'rand'
    METHOD_DISTANCE    = 'dist'

    def __init__(self):
        self.__ignored_keys = []


    #######################################################
    # K-MEANS CLUSTERING
    #
    # data   = Dataset to be clustered (list containing dictionarys)
    # k      = Number of clusters (integer)
    # dist   = Distance function (eucl=Euclidean | manh=Manhattan)
    # centre = Method for selecting the cluster centres (rand=Random | dist=Distance (furthest))
    #
    # updating clusters straight into the given data-object (dict)
    def kMeans(self, data, k=3, dist=DISTANCE_EUCLIDEAN, centre_method=METHOD_RANDOM, ignored_keys=[]):
        print("\nK-MEANS CLUSTERING:")

        # Take deepcopy of the data (don't want to edit the original dataset)
        data = deepcopy(data)

        dataCollector = []
        centerCollector = []

        # Keys (i.e values) that are ignored in classification computations (distances etc.)
        self.__ignored_keys.extend(ignored_keys)
        self.__ignored_keys.extend([self.CLUSTER_KEY, self.CLUSTER_DISTANCE_KEY])

        for i, case in enumerate(data):
            # Assigning each case into a cluster, which initially is itself
            case[self.CLUSTER_KEY] = "Case%d" % (i)
            case[self.CLUSTER_DISTANCE_KEY] = 0.0

            # TODO: Do this in preprocessing!
            # Turn attributes into floats:
            for att in self.dict_without_keys(case, self.__ignored_keys):
                case[att] = float(case[att])

        cluster_centres = self.__pickClusterCentres(centre_method, data, k)
        centerCollector.append(deepcopy(cluster_centres))

        while True:
            # Assign cluster for each case (if not any changes, break the loop)
            if self.__assignClusterCentres(data, cluster_centres, dist):
                # Update cluster centres by computing the mean values for each attribute
                self.__updateClusterCentres(cluster_centres, data)
                centerCollector.append(deepcopy(cluster_centres))
                dataCollector.append(deepcopy(data))
                print("\n   Updated cluster centroids -> New round with a loop...\n")
            else:
                dataCollector.append(deepcopy(data))
                print("\nNo changes, clustering job done!")
                break

        print()
        return (dataCollector, centerCollector)


    #######################################################
    # Picking the k cluster centroids with a given method
    #
    def __pickClusterCentres(self, method, data, k):
        c = []
        if method == self.METHOD_RANDOM:
            random.seed(12345) # Iris seems to work pretty well with seed 12345! (k=3, eucl)
            for i in range(k):
                c.append(dict( data[ random.randint(0, len(data)-1) ] ))
                # Remove unneccesary (for clusters) attributes
                for key in self.__ignored_keys:
                    c[i].pop(key, None)
                c[i][self.CLUSTER_KEY] = '%s%d' % (self.CLUSTER_NAME_PREFIX, i+1)
        elif method == self.METHOD_DISTANCE:
            # TODO ?:
            pass
        return c


    #######################################################
    # Assigns for each data point its closests cluster centre
    #
    def __assignClusterCentres(self, data, cluster_centres, dist, ):
        changes_made = False
        for i, case in enumerate(data):
            distances = self.__getDistances(case, cluster_centres, dist)
            closests_cluster = min(distances, key=distances.get)
            if case[self.CLUSTER_KEY] != closests_cluster:
                print("   UPDATE Case %d: (%s -> %s)" % (i, case[self.CLUSTER_KEY], closests_cluster))
                case[self.CLUSTER_KEY] = closests_cluster
                changes_made = True
            case[self.CLUSTER_DISTANCE_KEY] = distances[closests_cluster]
            print("   %d: %s" % (i, case))
        return changes_made


    #######################################################
    # Updates cluster centres
    # by computing the mean attribute values of cases in each cluster
    #
    def __updateClusterCentres(self, clusters, data):
        for cluster in clusters:
            # Initialize every attribute into 0.
            for att in self.dict_without_keys(cluster, self.__ignored_keys):
                cluster[att] = 0
            n = 0
            for case in data:
                if case[self.CLUSTER_KEY] == cluster[self.CLUSTER_KEY]:
                    # Add a value of each attribute of each case into a clusters corresponding attribute
                    for att in self.dict_without_keys(case, self.__ignored_keys):
                        cluster[att] += case[att]
                    n += 1

            if n > 0:
                # Divide added/summed attribute values with n (number of cases in a cluster) to get the mean of the values
                for att in self.dict_without_keys(cluster, self.__ignored_keys):
                    cluster[att] = cluster[att]/n


    #######################################################
    # Computes distances between one spesific case and
    # a list of cases. Returns dictionary of distances:
    # {'Cluster name': distance}
    def __getDistances(self, case, clusters, dist):
        distances = {}
        for cluster in clusters:

            if dist == self.DISTANCE_EUCLIDEAN:
                distances[cluster[self.CLUSTER_KEY]] = self.euclideanDist( \
                    list(self.dict_without_keys(case,    self.__ignored_keys).values()), \
                    list(self.dict_without_keys(cluster, self.__ignored_keys).values()))

            elif dist == self.DISTANCE_MANHATTAN:
                distances[cluster[self.CLUSTER_KEY]] = self.manhattanDist( \
                    list(self.dict_without_keys(case,    self.__ignored_keys).values()), \
                    list(self.dict_without_keys(cluster, self.__ignored_keys).values()))

            # TODO: Error: Given distance function not defined
            else:
                pass

        return distances


    #######################################################
    # Computes the EUCLIDEAN DISTANCE between two cases
    # param: Two lists of attribute values (float)
    # https://en.wikipedia.org/wiki/Euclidean_distance#Definition
    # sqrt( sum( (p_i-q_i)^2 ) )
    def euclideanDist(self, values1, values2):
        return sum([(p-q)**2 for p,q in zip(values1, values2)])**(0.5)


    #######################################################
    # Computes the MANHATTAN DISTANCE between two cases
    # param: Two lists of attribute values (float)
    # https://en.wikipedia.org/wiki/Taxicab_geometry#Formal_definition
    # sum(abs(p_i-q_i)
    def manhattanDist(self, values1, values2):
        return sum([abs(p-q) for p,q in zip(values1, values2)])


    #######################################################
    # Retuns a dictionary with given keys removed
    #
    def dict_without_keys(self, d, keys):
        return {x: d[x] for x in d if x not in keys}


    #######################################################
    # DENSITY-BASED CLUSTERING
    #
    def cluster_DBased(self, data):
        # TODO?
        pass
