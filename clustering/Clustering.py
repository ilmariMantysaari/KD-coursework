
class Clustering():
    DEVMODE = False

    CLUSTER_KEY          = 'cluster'
    CLUSTER_NAME_PREFIX  = 'CLUSTER'

    def __init__(self):
        self.filterKeys = []


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
    def dictionaryWithoutKeys(self, d, keys):
        return {x: d[x] for x in d if x not in keys}


    #######################################################
    # Computes distances between one spesific case and
    # a list of cases. Returns dictionary of distances:
    # {'Cluster name': distance}
    def getDistances(self, case, clusters, dist):
        distances = {}
        for cluster in clusters:

            if dist == self.DISTANCE_EUCLIDEAN:
                distances[cluster[self.CLUSTER_KEY]] = self.euclideanDist( \
                    list(self.dictionaryWithoutKeys(case,    self.filterKeys).values()), \
                    list(self.dictionaryWithoutKeys(cluster, self.filterKeys).values()))

            elif dist == self.DISTANCE_MANHATTAN:
                distances[cluster[self.CLUSTER_KEY]] = self.manhattanDist( \
                    list(self.dictionaryWithoutKeys(case,    self.filterKeys).values()), \
                    list(self.dictionaryWithoutKeys(cluster, self.filterKeys).values()))

            # TODO: Error: Given distance function not defined
            else:
                pass

        return distances
