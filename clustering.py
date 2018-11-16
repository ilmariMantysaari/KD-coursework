
import random
import copy

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
    def cluster_Kmeans(self, data, k=3, dist=DISTANCE_EUCLIDEAN, centre_method=METHOD_RANDOM):
        # Take deepcopy of the data (don't want to edit the original dataset)
        data = copy.deepcopy(data)
        print("\nK-MEANS CLUSTERING:")

        # TODO: Do this in preprocessing?
        for case in data:
            # Assigning each case into a cluster, which initially is itself
            case[CLUSTER_NAME] = case[CASE_NAME]
            case[CLUSTER_DISTANCE] = 0
            # Turn attributes into floats:
            for att in self.dict_without_keys(case, [CASE_NAME, CLUSTER_NAME]):
                case[att] = float(case[att])
        
        cluster_centres = self.pickClusterCentres(centre_method, data, k)
        
        changes_made = True
        while changes_made:
            changes_made = False

            # Assigning each case into a cluster whose centre is closest
            for case in data:
                distances = self.getDistances(case, cluster_centres, dist)
                closests_cluster = min(distances, key=distances.get)
                if case[CLUSTER_NAME] != closests_cluster:
                    print("   UPDATE %s (%s -> %s)" % (case[CASE_NAME], case[CLUSTER_NAME], closests_cluster))
                    case[CLUSTER_NAME] = closests_cluster
                    case[CLUSTER_DISTANCE] = distances[closests_cluster]
                    changes_made = True
                print("   %s: %s" % (case[CASE_NAME], case))

            # Update cluster centres by computing the mean values for each attribute
            if changes_made:
                self.updateClusterCentres(cluster_centres, data)
                print("\n   Updated cluster centroids -> New round with a loop...\n")
            else:
                print("\nNo changes, clustering job done!")

        print()
        return data


    #######################################################
    # Picking the k cluster centroids with a given method
    #
    def pickClusterCentres(self, method, data, k):
        c = []
        if method == self.METHOD_RANDOM:
            random.seed(123)
            for i in range(k):
                c.append(dict( data[ random.randint(0, len(data)-1) ] )) 
                c[i][CASE_NAME] = 'CLUSTER%d' % (i+1)
                # Remove unneccesary (for clusters) attributes
                c[i].pop('cluster', None)
                c[i].pop('dist', None)
        elif method == self.METHOD_DISTANCE:
            # TODO ?:
            pass
        return c


    #######################################################
    # Updates cluster centres 
    # by computing the mean attribute values of cases in each cluster
    #
    def updateClusterCentres(self, clusters, data):
        for cluster in clusters:
            # Initialize every attribute into 0.
            for att in self.dict_without_keys(cluster, [CASE_NAME]):
                cluster[att] = 0

            n = 0
            for case in data:
                if case['cluster'] == cluster[CASE_NAME]:
                    # Add a value of each attribute of each case into a clusters corresponding attribute
                    for att in self.dict_without_keys(case, [CASE_NAME, CLUSTER_NAME, CLUSTER_DISTANCE]):
                        cluster[att] += case[att]
                    n += 1

            # Divide added/summed attribute values with n (number of cases in a cluster) to get the mean of the values
            for att in self.dict_without_keys(cluster, [CASE_NAME]):
                cluster[att] = cluster[att]/n


    #######################################################
    # Computes distances between one spesific case and
    # a list of cases. Returns dictionary of distances:
    # {'Cluster name': distance}
    def getDistances(self, case, clusters, dist):
        distances = {}
        for cluster in clusters:

            if dist == self.DISTANCE_EUCLIDEAN:
                distances[cluster[CASE_NAME]] = self.euclideanDist( \
                    list(self.dict_without_keys(case,    [CASE_NAME, CLUSTER_NAME, CLUSTER_DISTANCE]).values()), \
                    list(self.dict_without_keys(cluster, [CASE_NAME, CLUSTER_NAME, CLUSTER_DISTANCE]).values()))

            elif dist == self.DISTANCE_MANHATTAN:
                distances[cluster[CASE_NAME]] = self.manhattanDist( \
                    list(self.dict_without_keys(case,    [CASE_NAME, CLUSTER_NAME, CLUSTER_DISTANCE]).values()), \
                    list(self.dict_without_keys(cluster, [CASE_NAME, CLUSTER_NAME, CLUSTER_DISTANCE]).values()))

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

