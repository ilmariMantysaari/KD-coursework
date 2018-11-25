#!/usr/bin/env python3

# from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import *
import preprocessing
import clustering
import copy
import csv
import output

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

            cluster = clustering.Clustering()
            datasCtrsTuple = cluster.kMeans(data, k=3, dist='eucl', centre_method='rand', ignored_keys=['Case', 'Cluster'])

            writer = output.ClusterImageWriter(self.filename)
            # Todo: use attributes keys set in UI
            writer.writeImages(datasCtrsTuple[0], datasCtrsTuple[1], 'cluster', 'dist2clu', 'petal_width', 'petal_length')


            print(self.filename)

root = Tk()
gui = ClusterGUI(root)
root.mainloop()
