
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
        # print("CLUSTERING/Data: %s" % (data))
        # print("CLUSTERING/K=%d" % (k))

        # TODO:
        # Arbitrarily pick K cases as initial cluster centres
        cluster_centres = [data[0], data[1]]
        centres_changed = True
        print(cluster_centres)
        while centres_changed:
            for case in data:
                # TODO:
                # Assign each case into a cluster whose centre is closest to the
                # case in the Euclidean/Manhattan distance sense
                for centre in cluster_centres:
                    self.euclideanDist(case, centre)
                    self.manhattanDist(case, centre)

                # TODO:
                # Compute for each cluster the mean vector of the points
                # assigned to the cluster. Use these mean vectors as new
                # cluster centres.
                centres_changed = False
        print(cluster_centres)
        print()
        return data

    #######################################################
    # Computes the EUCLIDEAN DISTANCE between two cases
    # https://en.wikipedia.org/wiki/Euclidean_distance#Definition
    # sqrt(sum(Qi - Pi)^2)
    def euclideanDist(self, case1, case2):
        if len(case1) != len(case2):
            return -1
        euc = 0;
        for i, att in enumerate(case1):
            if i > 0: # i.e. ignoring case names
                # TODO: Assuming now that all the data is float
                euc += ((float(case1[att])-float(case2[att]))**2)
        return euc**(0.5)

    #######################################################
    # Computes the MANHATTAN DISTANCE between two cases
    # https://en.wikipedia.org/wiki/Taxicab_geometry#Formal_definition
    # absolute value of sum(Qi-Pi)
    def manhattanDist(self, case1, case2):
        if len(case1) != len(case2):
            return -1
        man = 0;
        for i, att in enumerate(case1):
            if i > 0: # i.e. ignoring case names
                # TODO: Assuming now that all the data is float
                man += abs(float(case1[att])-float(case2[att]))
        return man**(0.5)



    #######################################################
    # DENSITY-BASED CLUSTERING
    #
    def cluster_DBased(self, data):
        # TODO?
        pass

