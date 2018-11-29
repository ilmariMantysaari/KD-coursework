from clustering.Clustering import Clustering
from copy import deepcopy

class DBSCAN(Clustering):

    DISTANCE_EUCLIDEAN = 'eucl'
    DISTANCE_MANHATTAN = 'manh'

    def __init__(self):
        super().__init__()

    # TODO:
    def cluster(eps, MinPts=4, dist=DISTANCE_EUCLIDEAN, filterKeys=[]):
        pass
