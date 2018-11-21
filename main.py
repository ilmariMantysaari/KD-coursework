#!/usr/bin/env python3

# from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import *
import preprocessing
import clustering
import copy
<<<<<<< HEAD
import csv

def main():
    # window = Tk()
    # textBox=Text(window, height=2, width=10)
    # textBox.pack()
    # buttonCommit=Button(window, height=1, width=10, text="Commit", 
    #                     command=lambda: retrieve_input())
    # buttonCommit.pack()
    filename = askopenfilename()
    with open(filename, 'r') as datafile:
        reader = csv.DictReader(datafile, delimiter=';')
        data = []
        for line in reader:
            data.append(line)

        pre = preprocessing.Preprocessing(data)
        pre.removeAttributes(["Att1", "Att3", "For example"])
        pre.normalizeData()

        cluster = clustering.Clustering()
        data_kmeans = cluster.kMeans(data, k=3, dist='eucl', centre_method='rand', ignored_keys=['Case', 'Cluster'])

        print(filename)

# if __name__ == "__main()__":
#     main()
main()


# clusterien määrä
# 
=======
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

            cluster = clustering.Clustering()
            data_kmeans = cluster.kMeans(data, k=3, dist='eucl', centre_method='rand', ignored_keys=['Case', 'Cluster'])

            print(self.filename)

root = Tk()
gui = ClusterGUI(root)
root.mainloop()
>>>>>>> 9c1f0f1faa9e9ebed190f76de069dbfff767f19d
