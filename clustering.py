
# TODO: Probably can't refer to a string 'Case' here (depends on dataset)
# (These constants should probably be someplace else anyway...)
CASE_NAME = 'Case'
CLUSTER_NAME = 'cluster'
CLUSTER_DISTANCE = 'dist'

class Clustering():

    EUC = 'euclidean'
    MAN = 'manhattan'

    def __init__(self):
        pass


    #######################################################
    # K-MEANS CLUSTERING
    #
    # data   = Dataset to be clustered
    # k      = Number of clusters (integer)
    # dist   = Distance function ("euclidean"/"manhattan")
    # centre = Method for selecting the cluster centres ("random/furthest")
    #
    def cluster_Kmeans(self, data, k=3, dist=EUC, centre='random'):
        print("\nK-MEANS:")

        # TODO: Do this in preprocessing?
        for case in data:
            # Assigning each case into a cluster, which initially is itself
            case[CLUSTER_NAME] = case[CASE_NAME]
            case[CLUSTER_DISTANCE] = 0
            for att in self.dict_without_keys(case, [CASE_NAME, CLUSTER_NAME]):
                case[att] = float(case[att])

        print(data)

        # TODO:
        # Arbitrarily pick K cases as initial cluster centres
        cluster_centres = [data[0], data[4]]

        centres_changed = True
        while centres_changed:
            centres_changed = False
            for case in data:

                # Assigning each case into a cluster whose centre is closest
                distances = self.getDistances(case, cluster_centres, dist)
                closests_cluster = min(distances, key=distances.get)
                if case[CLUSTER_NAME] != closests_cluster:
                    case[CLUSTER_NAME] = closests_cluster
                    case[CLUSTER_DISTANCE] = distances[closests_cluster]
                print("Clusters assigned! -> %s" % (case))

                # TODO:
                # Compute for each cluster the mean vector of the points
                # assigned to the cluster. Use these mean vectors as new
                # cluster centres.

                # centres_changed = True

        print()
        return data


    #######################################################
    # Computes distances between one spesific case and
    # a list of cases. Returns dictionary of distances:
    # {'Cluster name': distance}
    def getDistances(self, case, clusters, dist):
        distances = {}
        for cluster in clusters:

            # EUCLIDEAN DISTANCE
            if dist == self.EUC:
                distances[cluster[CASE_NAME]] = self.euclideanDist( \
                    list(self.dict_without_keys(case,    [CASE_NAME, CLUSTER_NAME]).values()), \
                    list(self.dict_without_keys(cluster, [CASE_NAME, CLUSTER_NAME]).values()))

            # MANHATTAN DISTANCE
            elif dist == self.MAN:
                distances[cluster[CASE_NAME]] = self.manhattanDist( \
                    list(self.dict_without_keys(case,    [CASE_NAME, CLUSTER_NAME]).values()), \
                    list(self.dict_without_keys(cluster, [CASE_NAME, CLUSTER_NAME]).values()))

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

