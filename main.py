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
from output import ClusterImageWriter

class ClusterGUI:

    def __init__(self, master):
        self.master = master
        self.filename = ""

        # distance buttons
        self.dist = StringVar(value="eucl")
        self.method = StringVar(value='rand')
        self.algorithm = StringVar(value='kmeans')

        Label(master, text = "Select distance function").grid(row=0, column=0)
        self.eucl_button = Radiobutton(master,
            text="k-means",
            variable=self.algorithm,
            selectcolor='red',
            value="kmeans")
        self.eucl_button.grid(row=1, column=0)
        self.manh_button = Radiobutton(master,
            text="DBSCAN",
            variable=self.algorithm,
            selectcolor='red',
            value="dbscan")
        self.manh_button.grid(row=2, column=0)

        Label(master, text = "Select distance function").grid(row=3, column=0)
        self.eucl_button = Radiobutton(master,
            text="Euclidean",
            selectcolor='red',
            variable=self.dist,
            value= kMeans.DISTANCE_EUCLIDEAN)
        self.eucl_button.grid(row=4, column=0)
        self.manh_button = Radiobutton(master,
            text="Manhattan",
            selectcolor='red',
            variable=self.dist,
            value= kMeans.DISTANCE_MANHATTAN)
        self.manh_button.grid(row=5, column=0)

        # method
        Label(master, text = "Select method function").grid(row=6, column=0)
        self.rand_button = Radiobutton(master, 
            text="Random",
            variable=self.method,
            selectcolor='red',
            value= kMeans.METHOD_RANDOM)
        self.rand_button.grid(row=7, column=0)
        self.dist_button = Radiobutton(master,
            text="Distance",
            variable=self.method,
            selectcolor='red',
            value= kMeans.METHOD_DISTANCE)
        self.dist_button.grid(row=8, column=0)

        self.filename_select = Button(master, text="Select file", command=self.get_filename)
        self.filename_select.grid(row=9, column=0)

        self.filename_text = Label(master, wraplength=250)
        self.filename_text.grid(row=10, column=0)

        self.cluster_button = Button(master, text="Cluster", command=self.clustering)
        self.cluster_button.grid(row=11, column=1)

    def get_filename(self):
        self.filename = askopenfilename()
        self.filename_text.config(text=self.filename)

    def clustering(self):
        with open(self.filename, 'r') as datafile:
            reader = csv.DictReader(datafile, delimiter=';')
            data = []
            for line in reader:
                data.append(line)

            pre = preprocessing.Preprocessing(data)
            #pre.removeAttributes(["Att1", "Att3", "For example"])
            normalized_data = pre.normalizeData()

            k_means = kMeans()
            dbscan = DBSCAN()
            if self.algorithm == 'kmeans':
                data_kmeans = k_means.cluster(normalized_data, k=3, 
                    dist=self.dist.get(),
                    centreMethod=self.method.get,
                    filterKeys=['Case', 'class'])
            else:
                data_dbscan = dbscan.cluster(normalized_data, eps=1.2,
                    MinPts=3,
                    dist='eucl',
                    filterKeys=['Case', 'class'])
            
            pp = pprint.PrettyPrinter(indent=2)
            #pp.pprint(data_kmeans)
            # Cluster centres and clustered data listed in every iteration:
            #pp.pprint(k_means.iterCentres)
            #pp.pprint(k_means.iterData)

            print(self.filename)
            clustWriter = ClusterImageWriter("newfile")
            # clustWriter.

root = Tk()
gui = ClusterGUI(root)
root.mainloop()



# csv output
# valikot
# giffin tulostus
# loput inputit
# preprocessingille asetukset

# attribuutin valinta
    # vain numeerisia attribuutteja

# näytä giffi ja kuva kun valmista


