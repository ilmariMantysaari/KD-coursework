#!/usr/bin/env python3

# from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import *
import preprocessing
import clustering
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
        reader = csv.reader(datafile, delimiter=';')
        data = list(reader)   
        # TODO: Get data as a dictionary instead if a list ?

        pre = preprocessing.Preprocessing(data)
        pre.removeAttributes(["Att1", "Att3"])
        pre.normalizeData()

        c = clustering.Clustering()
        c.cluster_Kmeans(data, k=2, dist="manhattan", centre="random")

        print(filename)

# if __name__ == "__main()__":
#     main()
main()


# clusterien määrä
# 