
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
    # updating clusters straight into the given data-object (dict)
    def cluster_Kmeans(self, data, k=3, dist=EUC, centre_method='random'):
        print("\nK-MEANS CLUSTERING:")

        # TODO: Do this in preprocessing?
        for case in data:
            # Assigning each case into a cluster, which initially is itself
            case[CLUSTER_NAME] = case[CASE_NAME]
            case[CLUSTER_DISTANCE] = 0
            # Turn attributes into floats:
            for att in self.dict_without_keys(case, [CASE_NAME, CLUSTER_NAME]):
                case[att] = float(case[att])

        # TODO:
        # Arbitrarily pick K cases as initial cluster centres
        # Use dict(x) to get copys of dictionarys
        cluster_centres = [dict(data[1]), dict(data[2])] 
        cluster_centres[0]['Case'] = 'CLUSTER1'
        cluster_centres[1]['Case'] = 'CLUSTER2'
        # Remove unneccesary attributes
        cluster_centres[0].pop('cluster', None)
        cluster_centres[1].pop('cluster', None)
        cluster_centres[0].pop('dist', None)
        cluster_centres[1].pop('dist', None)

        changes_made = True
        while changes_made:
            changes_made = False

            # Assigning each case into a cluster whose centre is closest
            for case in data:
                distances = self.getDistances(case, cluster_centres, dist)
                closests_cluster = min(distances, key=distances.get)
                if case[CLUSTER_NAME] != closests_cluster:
                    print("   UPDATE (%s != %s)" % (case[CLUSTER_NAME], closests_cluster))
                    case[CLUSTER_NAME] = closests_cluster
                    case[CLUSTER_DISTANCE] = distances[closests_cluster]
                    changes_made = True
                print("   Clusters assigned! -> %s" % (case))

            # Update cluster centres by computing the mean values for each attribute
            if changes_made:
                self.updateClusterCentres(cluster_centres, data)
                print("\n   Updated cluster centroids -> New round with a loop...\n")
            else:
                print("\nNo changes, clustering job done!")

        print()



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

            # EUCLIDEAN DISTANCE
            if dist == self.EUC:
                distances[cluster[CASE_NAME]] = self.euclideanDist( \
                    list(self.dict_without_keys(case,    [CASE_NAME, CLUSTER_NAME, CLUSTER_DISTANCE]).values()), \
                    list(self.dict_without_keys(cluster, [CASE_NAME, CLUSTER_NAME, CLUSTER_DISTANCE]).values()))

            # MANHATTAN DISTANCE
            elif dist == self.MAN:
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

