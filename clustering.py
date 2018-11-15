
class Clustering():

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
    def cluster_Kmeans(self, data, k=3, dist="euclidean", centre="random"):
        print("\nK-MEANS:")
        print("CLUSTERING/Data: %s" % (data))
        print("CLUSTERING/K=%d" % (k))

        # TODO:
        # Arbitrarily pick K cases as initial cluster centres
        cluster_centres = [data[1]]
        centres_changed = True
        print(cluster_centres)
        while centres_changed:
            for case in data:
                # TODO:
                # Assign each case into a cluster whose centre is closest to the
                # case in the Euclidean/Manhattan distance sense

                # TODO:
                # Compute for each cluster the mean vector of the points
                # assigned to the cluster. Use these mean vectors as new
                # cluster centres.
                centres_changed = False

        return data

    # Computes the Euclidean distance between two cases
    def euclideanDist(self, case1, case2):
        # TODO:
        pass

    # Computes the Manhattan distance between two cases
    def manhattanDist(self, case1, case2):
        # TODO:
        pass



    #######################################################
    # DENSITY-BASED CLUSTERING
    #
    def cluster_DBased(self, data):
        # TODO?
        pass

