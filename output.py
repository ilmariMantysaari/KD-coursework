# Class for outputtings simple scatter plot images of clustersself.
# Create a new instance for each clustering job.
import copy
import datetime
import glob
import imageio
import matplotlib.pyplot as plt


# Utility method for finding unique cluster names from data
def parseClusterNames(data, clusterKey):
    clusterNames = map(lambda case: case[clusterKey], data)
    uniqClusterNames = list(set(clusterNames))
    uniqClusterNames.sort()
    return uniqClusterNames


class ClusterImageWriter():
    DEFAULT_COLORS = ['firebrick', 'gray', 'blue', 'plum', 'olive', 'dodgerblue', 'fuchsia', 'green', 'aqua', 'midnightblue']
    DEFAULT_GIF_DELAY = 1
    MAX_MARKER_SIZE = 13
    MIN_MARKER_SIZE = 3
    CENTER_SIZE = 7

    # INIT
    # Set some variables here for file names
    def __init__(self, fileName, suffix=datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')):
        self.fileName = fileName
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
    def writeImages(self, dataList, centersList, clusterKey, distanceKey, xAttr, yAttr, colors=DEFAULT_COLORS):
        for i in range(0, len(dataList)):
            self.writeImage(dataList[i], centersList[i], clusterKey, distanceKey, xAttr, yAttr, self.imgCounter, colors)
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
    def writeImage(self, data, centers, clusterKey, distanceKey, xAttr, yAttr, imgNum, colors=DEFAULT_COLORS):
        # Don't edit original data
        dataC = copy.deepcopy(data)
        centersC = copy.deepcopy(centers)
        clusterNames = parseClusterNames(dataC, clusterKey)
        colorI = 0
        # Iterate through cluster names so that each cluster gets different color
        for name in clusterNames:
            clusterCases = list(filter(lambda case: case[clusterKey] == name, dataC))
            center = list(filter(lambda cpoint: cpoint[clusterKey] == name, centersC))[0]
            safeColorI = colorI % len(colors)

            # Marker size will be relative to distance from cluster center
            maxDist = max(map(lambda case: case[distanceKey], clusterCases))
            sizeRange = self.MAX_MARKER_SIZE - self.MIN_MARKER_SIZE

            for case in clusterCases:
                caseMarkerSize = self.MAX_MARKER_SIZE - ((case[distanceKey] / maxDist) * sizeRange)
                plt.plot(case[xAttr], case[yAttr], color=colors[safeColorI], marker='o', markersize=caseMarkerSize)

            # Draw cluster center last
            plt.plot(center[xAttr], center[yAttr], color=colors[safeColorI], marker='D', markerSize=self.CENTER_SIZE, markeredgecolor='black')
            colorI = colorI + 1

        # Output a file and clear the figure
        fileName = self.id + '_' + str(imgNum) + ".png"
        plt.title("'" + self.fileName + "' - phase " + str(self.imgCounter))
        plt.ylabel(yAttr)
        plt.xlabel(xAttr)
        plt.savefig(fileName, format='png')
        plt.clf()
        return

    # COMBINE ALL IMAGES MADE BY THIS WRITER TO A GIF
    def writeGif(self):
        imgFiles = glob.glob(self.id + "*.png")
        images = map(lambda file: imageio.imread(file), imgFiles)
        imageio.mimsave(self.id + "_combined.gif", images, duration=1.5)
        return
