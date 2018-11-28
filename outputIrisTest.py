import csv
from clustering.kMeans import kMeans
import glob
import output
import os
import pathlib
import preprocessing
import unittest


class TestClusterOutput(unittest.TestCase):

    # Clean up iris output files
    def setup(self):
        imgFiles = glob.glob('iris.csv_output' + '*.png')
        imgFiles.append('iris.csv_output_combined.gif')
        for fileName in imgFiles:
            if pathlib.Path(fileName).is_file():
                os.remove(fileName)

    def test_irisDataOutput(self):
        with open('iris.csv', 'r') as datafile:
            reader = csv.DictReader(datafile, delimiter=';')
            data = []
            for line in reader:
                data.append(line)

            pre = preprocessing.Preprocessing(data)
            normalizedData = pre.normalizeData()

            k_means = kMeans()
            data_kmeans = k_means.cluster(normalizedData, k=3, dist='eucl', centreMethod='rand', filterKeys=['Case', 'class'])

            writer = output.ClusterImageWriter('iris.csv', 'output')
            writer.writeImages(k_means.iterData, k_means.iterCentres, 'cluster', 'dist2clu', 'petal_width', 'petal_length')
            writer.writeGif()
