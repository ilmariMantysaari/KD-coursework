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

    # WRITE MULTIPLE IMAGES FOR DIFFERENT CLUSTER PHASES
    #
    # dataList   = List of clustered data in different phases of clustering. Check outputTest.py for example.
    # clusterKey = Key for cluster attribute in each case
    # xAttr      = Key for x-axis attribute in the resulting image. Also the label for x-axis
    # yAttr      = Key for y-axis attribute in the resulting image. Also the label for y-axis
    # colors     = [Optional] Color codes for clusters. If there's more clusters
    #              than color codes, the list is started from the beginning.
    #              https://matplotlib.org/examples/color/named_colors.html
    def writeImages(self, dataList, clusterKey, xAttr, yAttr, colors=DEFAULT_COLORS):
        for data in dataList:
            self.writeImage(data, clusterKey, xAttr, yAttr, self.imgCounter, colors)
            self.imgCounter = self.imgCounter + 1
        return

    # WRITE SINGLE IMAGE
    #
    # data       = Dataset to be rendered. Represents one phase in clustering
    # clusterKey = Key for cluster attribute in each case
    # xAttr      = Key for x-axis attribute in the resulting image. Also the label for x-axis
    # yAttr      = Key for y-axis attribute in the resulting image. Also the label for y-axis
    # colors     = Color codes for clusters
    # imgNum     = Numeric counter appended to outputted file's name
    def writeImage(self, data, clusterKey, xAttr, yAttr, imgNum, colors=DEFAULT_COLORS):
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
        fileName = self.id + '_' + str(imgNum) + ".png"
        plt.savefig(fileName, format='png')
        # Todo: remove show call from finished solution
        plt.show()
        return

    # COMBINE ALL IMAGES MADE BY THIS WRITER TO A GIF
    def writeGif(delay=DEFAULT_GIF_DELAY):
        return
