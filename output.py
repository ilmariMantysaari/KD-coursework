# Class for outputtings simple scatter plot images of clustersself.
# Create a new instance for each clustering job.
import copy
import datetime
import matplotlib.pyplot as plt


# Utility method for finding unique cluster names from data
def parseClusterNames(data, clusterKey):
    clusterNames = map(lambda case: case[clusterKey], data)
    uniqClusterNames = list(set(clusterNames))
    uniqClusterNames.sort()
    return uniqClusterNames


class ClusterImageWriter():
    DEFAULT_COLORS = ['firebrick', 'chartreuse', 'blue', 'plum', 'olive', 'dodgerblue', 'fuchsia', 'green', 'aqua', 'midnightblue']
    DEFAULT_GIF_DELAY = 1

    # INIT
    # Set some variables here for file names
    def __init__(self, fileName, suffix=datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')):
        self.id = fileName + '_' + suffix
        self.imgCounter = 1

    # WRITE SINGLE IMAGE
    #
    # data       = Dataset to be rendered (list containing dictionarys)
    # clusterKey = Key for cluster attribute in each case
    # xAttr      = Key for x-axis attribute in the resulting image
    # xLabel     = Label for x-axis in the resulting image
    # yAttr      = Key for y-axis attribute in the resulting image
    # yLabel     = Label for y-axis in the resulting image
    # colors     = [Optional] Color codes for clusters. If there's more clusters
    #              than color codes, the list is started from the beginning.
    #              https://matplotlib.org/examples/color/named_colors.html
    def writeImage(self, data, clusterKey, xAttr, xLabel, yAttr, yLabel, colors=DEFAULT_COLORS):
        # Don't edit original data
        dataC = copy.deepcopy(data)
        clusterNames = parseClusterNames(dataC, clusterKey)
        colorI = 0
        # Iterate through cluster names so that each cluster gets different color
        for name in clusterNames:
            clusterCases = filter(lambda case: case[clusterKey] == name, dataC)
            safeColorI = colorI % len(colors)
            for case in clusterCases:
                plt.plot(case[xAttr], case[yAttr], color=colors[safeColorI], marker='o', markersize=5)
            colorI = colorI + 1
        fileName = self.id + '_' + str(self.imgCounter) + ".png"
        plt.savefig(fileName, format='png')
        self.imgCounter = self.imgCounter + 1
        # Todo: remove show call from finished solution
        plt.show()
        return

    # COMBINE ALL IMAGES MADE BY THIS WRITER TO A GIF
    def writeGif(delay=DEFAULT_GIF_DELAY):
        return
