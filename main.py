#!/usr/bin/env python3

# from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import *
import preprocessing
import clustering
import copy
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

        clu = clustering.Clustering()
        clustered_data_kmeans = clu.cluster_Kmeans(data, k=3, dist="eucl", centre_method="rand")

        print(filename)

# if __name__ == "__main()__":
#     main()
main()


# clusterien määrä
# 