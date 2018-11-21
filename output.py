# Class for outputtings simple scatter plot images of clustersself.
# Create a new instance for each clustering job.
import datetime


class ClusterImageWriter():
    DEFAULT_COLORS = ['firebrick', 'chartreuse', 'blue', 'plum', 'olive', 'dodgerblue', 'fuchsia', 'green', 'aqua', 'midnightblue']
    DEFAULT_GIF_DELAY = 1

    # Set some variables used in building filenames on init
    def __init__(self, fileName):
        date = datetime.datetime.now()
        self.id = fileName + date.strftime('_%Y_%m_%d__%H_%M_%S')
        self.counter = 1

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
    def writeImage(data, clusterKey, xAttr, xLabel, yAttr, yLabel, colors=DEFAULT_COLORS):
        return

    # COMBINE ALL IMAGES MADE BY THIS WRITER TO A GIF
    def writeGif(delay=DEFAULT_GIF_DELAY):
        return
