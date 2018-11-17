
import random
from copy import deepcopy

# TODO: Probably can't refer to a string 'Case' here (depends on dataset)
# (These constants should probably be someplace else anyway...)
CASE_NAME = 'Case'
CLUSTER_NAME = 'cluster'
CLUSTER_DISTANCE = 'dist2clu'

class Clustering():

    DISTANCE_EUCLIDEAN = 'eucl'
    DISTANCE_MANHATTAN = 'manh'
    METHOD_RANDOM      = 'rand'
    METHOD_DISTANCE    = 'dist'

    def __init__(self):
        pass


    #######################################################
    # K-MEANS CLUSTERING
    #
    # data   = Dataset to be clustered (list containing dictionarys)
    # k      = Number of clusters (integer)
    # dist   = Distance function (eucl=Euclidean | manh=Manhattan)
    # centre = Method for selecting the cluster centres (rand=Random | dist=Distance (furthest))
    #
    # updating clusters straight into the given data-object (dict)
    def cluster_Kmeans(self, data, k=3, dist=DISTANCE_EUCLIDEAN, centre_method=METHOD_RANDOM, ignored_keys=[]):
        print("\nK-MEANS CLUSTERING:")

        # Take deepcopy of the data (don't want to edit the original dataset)
        data = deepcopy(data)
        
        ignored_keys.append(CLUSTER_NAME)
        ignored_keys.append(CLUSTER_DISTANCE)

        for i, case in enumerate(data):
            # Assigning each case into a cluster, which initially is itself
            case[CLUSTER_NAME] = "Case%d" % (i)
            case[CLUSTER_DISTANCE] = 0.0
            
            # TODO: Do this in preprocessing!
            # Turn attributes into floats:
            for att in self.dict_without_keys(case, ignored_keys):
                case[att] = float(case[att])
        
        cluster_centres = self.pickClusterCentres(centre_method, data, k, ignored_keys)
        
        while True:
            # Assign cluster for each case (if not any changes, break the loop)
            if self.assignClusterCentres(data, cluster_centres, dist, ignored_keys):
                # Update cluster centres by computing the mean values for each attribute
                self.updateClusterCentres(cluster_centres, data, ignored_keys)
                print("\n   Updated cluster centroids -> New round with a loop...\n")
            else:
                print("\nNo changes, clustering job done!")
                break

        print()
        return data


    #######################################################
    # Picking the k cluster centroids with a given method
    #
    def pickClusterCentres(self, method, data, k, ignored_keys):
        c = []
        if method == self.METHOD_RANDOM:
            random.seed(123)
            for i in range(k):
                c.append(dict( data[ random.randint(0, len(data)-1) ] )) 
                # Remove unneccesary (for clusters) attributes
                for key in ignored_keys:
                    c[i].pop(key, None)
                c[i][CLUSTER_NAME] = 'CLUSTER%d' % (i+1)
        elif method == self.METHOD_DISTANCE:
            # TODO ?:
            pass
        return c


    #######################################################
    # Assigns for each data point its closests cluster centre
    #
    def assignClusterCentres(self, data, cluster_centres, dist, ignored_keys):
        changes_made = False
        for i, case in enumerate(data):
            distances = self.getDistances(case, cluster_centres, dist, ignored_keys)
            closests_cluster = min(distances, key=distances.get)
            if case[CLUSTER_NAME] != closests_cluster:
                print("   UPDATE Case %d: (%s -> %s)" % (i, case[CLUSTER_NAME], closests_cluster))
                case[CLUSTER_NAME] = closests_cluster
                case[CLUSTER_DISTANCE] = distances[closests_cluster]
                changes_made = True
            print("   %d: %s" % (i, case))
        return changes_made


    #######################################################
    # Updates cluster centres 
    # by computing the mean attribute values of cases in each cluster
    #
    def updateClusterCentres(self, clusters, data, ignored_keys):
        for cluster in clusters:
            # Initialize every attribute into 0.
            for att in self.dict_without_keys(cluster, ignored_keys):
                cluster[att] = 0
            n = 0
            for case in data:
                if case[CLUSTER_NAME] == cluster[CLUSTER_NAME]:
                    # Add a value of each attribute of each case into a clusters corresponding attribute
                    for att in self.dict_without_keys(case, ignored_keys):
                        cluster[att] += case[att]
                    n += 1

            if n > 0:
                # Divide added/summed attribute values with n (number of cases in a cluster) to get the mean of the values
                for att in self.dict_without_keys(cluster, ignored_keys):
                    cluster[att] = cluster[att]/n


    #######################################################
    # Computes distances between one spesific case and
    # a list of cases. Returns dictionary of distances:
    # {'Cluster name': distance}
    def getDistances(self, case, clusters, dist, ignored_keys):
        distances = {}
        for cluster in clusters:

            if dist == self.DISTANCE_EUCLIDEAN:
                distances[cluster[CLUSTER_NAME]] = self.euclideanDist( \
                    list(self.dict_without_keys(case,    ignored_keys).values()), \
                    list(self.dict_without_keys(cluster, ignored_keys).values()))

            elif dist == self.DISTANCE_MANHATTAN:
                distances[cluster[CLUSTER_NAME]] = self.manhattanDist( \
                    list(self.dict_without_keys(case,    ignored_keys).values()), \
                    list(self.dict_without_keys(cluster, ignored_keys).values()))

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
        return sum([(p-q)**2 for p,q in zip(values1, values2)])


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

