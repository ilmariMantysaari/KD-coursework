#!/usr/bin/env python3

# from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import *
import preprocessing
import clustering
import copy
import csv     

class ClusterGUI:
    def __init__(self, master):
        self.master = master
        self.filename = ""

        # distance buttons
        self.dist = StringVar()
        Label(master, text = "Select distance function").pack()
        self.eucl_button = Radiobutton(master, text="Euclidean",
            variable=self.dist, value= clustering.Clustering.DISTANCE_EUCLIDEAN)
        self.eucl_button.pack()
        self.manh_button = Radiobutton(master, text="Manhattan",
            variable=self.dist, value= clustering.Clustering.DISTANCE_MANHATTAN)
        self.manh_button.pack()

        # method
        self.method = StringVar()
        Label(master, text = "Select method function").pack()
        self.rand_button = Radiobutton(master, text="Random",
            variable=self.method, value= clustering.Clustering.METHOD_RANDOM)
        self.rand_button.pack()
        self.dist_button = Radiobutton(master, text="Distance",
            variable=self.method, value= clustering.Clustering.METHOD_DISTANCE)
        self.dist_button.pack()

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
            data_kmeans = cluster.kMeans(data, k=3, dist=self.dist, centre_method=self.method, ignored_keys=['Case', 'Cluster'])

            print(self.filename)

            # piirrä clusteri
            print(data_kmeans)

root = Tk()
gui = ClusterGUI(root)
root.mainloop()

# valinnat clusteringin parametreille
    # checkboxit vivuille
    # näytä tiedoston nimi
    # k:n valinta
# mahd. valinta poistetaville attribuuteille
# clustereiden näyttö
    # clusteri graafi
# clustereista tietoa
    # määrä
    # caset/clusteri
    # centroidit

