# Class for outputtings simple scatter plot images of clustersself.
# Create a new instance for each clustering job.
import copy
import datetime
import glob
import imageio
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# Utility method for finding unique cluster names from data
def parseClusterNames(data, clusterKey):
    clusterNames = map(lambda case: case[clusterKey], data)
    uniqClusterNames = list(set(clusterNames))
    uniqClusterNames.sort()
    return uniqClusterNames


class ClusterImageWriter():
    DEFAULT_COLORS = ['firebrick', 'darkgreen', 'blue', 'plum', 'olive', 'dodgerblue', 'fuchsia', 'limegreen', 'aqua', 'midnightblue']
    DEFAULT_GIF_DELAY = 1
    MAX_MARKER_SIZE = 13
    MIN_MARKER_SIZE = 3
    DBSCAN_MARKER_SIZE = 5
    POINT_MARKER = 'o'
    CENTER_MARKER = 'D'
    CENTER_SIZE = 7
    CENTER_COLOR = 'white'

    # INIT
    # Set some variables here for file names
    def __init__(self, fileName, suffix=datetime.datetime.now().strftime('%Y_%m_%d__%H_%M_%S')):
        self.fileName = fileName
        self.id = fileName + '_' + suffix
        self.imgCounter = 1

    # WRITE MULTIPLE IMAGES FOR DIFFERENT CLUSTER PHASES FOR K-MEANS CLUSTERING
    #
    # dataList   = List of clustered data in different phases of clustering. Check outputTest.py for example.
    # clusterKey = Key for cluster attribute in each case
    # xAttr      = Key for x-axis attribute in the resulting image. Also the label for x-axis
    # yAttr      = Key for y-axis attribute in the resulting image. Also the label for y-axis
    # colors     = [Optional] Color codes for clusters. If there's more clusters
    #              than color codes, the list is started from the beginning.
    #              https://matplotlib.org/examples/color/named_colors.html
    def writeKMeansImages(self, dataList, centersList, clusterKey, distanceKey, xAttr, yAttr, colors=DEFAULT_COLORS):
        names = []
        for i in range(0, len(dataList)):
            names.append(self.writeKMeansImage(dataList[i], centersList[i], clusterKey, distanceKey, xAttr, yAttr, self.imgCounter, colors))
            self.imgCounter = self.imgCounter + 1
        return names

    # WRITE SINGLE IMAGE
    #
    # data       = Dataset to be rendered. Represents one phase in clustering
    # clusterKey = Key for cluster attribute in each case
    # xAttr      = Key for x-axis attribute in the resulting image. Also the label for x-axis
    # yAttr      = Key for y-axis attribute in the resulting image. Also the label for y-axis
    # colors     = Color codes for clusters
    # imgNum     = Numeric counter appended to outputted file's name
    def writeKMeansImage(self, data, centers, clusterKey, distanceKey, xAttr, yAttr, imgNum, colors=DEFAULT_COLORS):
        # Don't edit original data
        dataC = copy.deepcopy(data)
        centersC = copy.deepcopy(centers)
        clusterNames = parseClusterNames(dataC, clusterKey)
        colorI = 0
        legends = []
        # Iterate through cluster names so that each cluster gets different color
        for name in clusterNames:
            clusterCases = list(filter(lambda case: case[clusterKey] == name, dataC))
            center = list(filter(lambda cpoint: cpoint[clusterKey] == name, centersC))[0]
            safeColorI = colorI % len(colors)
            color = colors[safeColorI]

            # Marker size will be relative to distance from cluster center
            maxDist = max(map(lambda case: case[distanceKey], clusterCases))
            sizeRange = self.MAX_MARKER_SIZE - self.MIN_MARKER_SIZE

            for case in clusterCases:
                caseMarkerSize = self.MAX_MARKER_SIZE - ((case[distanceKey] / maxDist) * sizeRange)
                plt.plot(case[xAttr], case[yAttr], color=color, marker=self.POINT_MARKER, markersize=caseMarkerSize)

            # Draw cluster center last
            plt.plot(center[xAttr], center[yAttr], color=self.CENTER_COLOR, marker=self.CENTER_MARKER, markerSize=self.CENTER_SIZE, markeredgewidth=2, markeredgecolor=color)
            colorI = colorI + 1

            # Add legend
            label = name + ', n=' + str(len(clusterCases))
            legends.append(mpatches.Patch(color=color, label=label))

        # Output a file and clear the figure
        fileName = self.id + '_' + str(imgNum) + ".png"
        plt.title("'" + self.fileName + "' - phase " + str(self.imgCounter))
        plt.legend(handles=legends)
        plt.ylabel(yAttr)
        plt.xlabel(xAttr)
        plt.savefig(fileName, format='png')
        plt.clf()
        return fileName

    # WRITE OUTPUT FOR A DBSCAN CLUSTERING - ONLY ONE IMAGE PER RESULT
    #
    #
    #
    def writeDBSCANImage(self, data, clusterKey, xAttr, yAttr, minPts, eps, colors=DEFAULT_COLORS):
        # Don't edit original data
        dataC = copy.deepcopy(data)
        clusterNames = parseClusterNames(dataC, clusterKey)
        colorI = 0
        legends = []

        # Iterate through cluster names so that each cluster gets different color
        for name in clusterNames:
            clusterCases = list(filter(lambda case: case[clusterKey] == name, dataC))
            safeColorI = colorI % len(colors)
            color = colors[safeColorI]

            for case in clusterCases:
                plt.plot(case[xAttr], case[yAttr], color=colors[safeColorI], marker=self.POINT_MARKER, markersize=self.DBSCAN_MARKER_SIZE)

            colorI = colorI + 1

            # Add legend
            label = name + ', n=' + str(len(clusterCases))
            legends.append(mpatches.Patch(color=color, label=label))

        # Output a file and clear the figure
        fileName = self.id + '_DBSCAN' + ".png"
        plt.title("'" + self.fileName + "' - DBSCAN, Minpts=" + str(minPts) + ", Eps=" + str(eps))
        plt.legend(handles=legends)
        plt.ylabel(yAttr)
        plt.xlabel(xAttr)
        plt.savefig(fileName, format='png')
        plt.clf()
        return fileName

    # COMBINE ALL IMAGES MADE BY THIS WRITER TO A GIF
    def writeGif(self):
        imgFiles = glob.glob(self.id + "*.png")
        imgFiles.sort()
        images = map(lambda file: imageio.imread(file), imgFiles)
        imageio.mimsave(self.id + "_combined.gif", images, duration=1.5)
        return self.id + "_combined.gif"
