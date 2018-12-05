import csv
from clustering.DBSCAN import DBSCAN
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

            dbscanner = DBSCAN()
            data = dbscanner.cluster(normalizedData, 0.065, 4, 'eucl', ['Case', 'class', 'sepal_width', 'sepal_length'])

            writer = output.ClusterImageWriter('iris.csv', 'output')
            writer.writeDBSCANImage(data, 'cluster', 'petal_width', 'petal_length', 4, 0.07)
