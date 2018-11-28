#!/usr/bin/env python3

# from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import *
import preprocessing
from clustering.kMeans import kMeans
from clustering.DBSCAN import DBSCAN
import pprint
import copy
import csv

class ClusterGUI:
    def __init__(self, master):
        self.master = master
        self.filename = ""

        self.filename_select = Button(master, text="Select file", command=self.get_filename)
        self.filename_select.pack()

        self.cluster_button = Button(master, text="Cluster", command=self.clustering)
        self.cluster_button.pack()

    def get_filename(self):
        self.filename = askopenfilename()

    def clustering(self):
        with open(self.filename, 'r') as datafile:
            reader = csv.DictReader(datafile, delimiter=';')
            data = []
            for line in reader:
                data.append(line)

            pre = preprocessing.Preprocessing(data)
            pre.removeAttributes(["Att1", "Att3", "For example"])
            pre.normalizeData()

            k_means = kMeans()
            data_kmeans = k_means.cluster(data, k=3, dist='eucl', centreMethod='rand', filterKeys=['Case', 'class'])
            
            pp = pprint.PrettyPrinter(indent=2)
            pp.pprint(data_kmeans)
            # Cluster centres and clustered data listed in every iteration:
            #pp.pprint(k_means.iterCentres)
            #pp.pprint(k_means.iterData)

            print(self.filename)

root = Tk()
gui = ClusterGUI(root)
root.mainloop()
