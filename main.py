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
from PIL import ImageTk, Image

def is_int(text):
    try:
        int(text)
        return True
    except ValueError:
        return False

def is_float(text):
    try:
        float(text)
        return True
    except ValueError:
        return False

class ClusterGUI:

    def __init__(self, master):
        self.master = master
        self.data = []
        self.filename = ""

        # distance buttons
        self.dist = StringVar(value="eucl")
        self.method = StringVar(value='rand')
        self.algorithm = StringVar(value='kmeans')
        self.attributes = []
        self.boxes = []

        Label(master, text = "Select algorithm").grid(row=0, column=0)
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

        Label(master, text="k:").grid(row=1, column=4)
        self.k_entry = Entry(master)
        self.k_entry.grid(row=2, column=4)

        Label(master, text="MinPts:").grid(row=4, column=4)
        self.min_pts_entry = Entry(master)
        self.min_pts_entry.grid(row=5, column=4)

        Label(master, text="Eps:").grid(row=7, column=4)
        self.eps_entry = Entry(master)
        self.eps_entry.grid(row=8, column=4)

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

        self.filename_select = Button(master, text="Select file", command=self.get_filename)
        self.filename_select.grid(row=9, column=0)

        self.filename_text = Label(master, wraplength=250)
        self.filename_text.grid(row=10, column=0)

        self.error_text = Label(master, wraplength=250)
        self.error_text.grid(row=8, column=4)

        self.cluster_button = Button(master, text="Cluster", command=self.clustering)
        self.cluster_button.grid(row=11, column=1)

        self.image_frame = Label(master)
        self.image_frame.grid(row=1, column=6)

    def get_data(self):
        with open(self.filename, 'r') as datafile:
            reader = csv.DictReader(datafile, delimiter=';')
            for line in reader:
                self.data.append(line)

            self.attributes = reader.fieldnames
            checks = []

            for att in reader.fieldnames:
                var = IntVar()
                checks.append(var)
                l = Checkbutton(self.master, text=att, variable=var, selectcolor='red')
                print(var.get())
                l.grid()

            self.boxes = checks

    def get_filename(self):
        self.filename = askopenfilename()
        self.filename_text.config(text=self.filename)
        self.get_data()

    def clustering(self):
        # check input validity
        if not self.filename:
            self.error_text.config(text="Choose a file first")
            return
        if self.algorithm.get() == 'kmeans' and not is_int(self.k_entry.get()):
            self.error_text.config(text="Select k")
            return
        if self.algorithm.get() == 'dbscan' and not is_int(self.min_pts_entry.get()) and not is_float(self.eps_entry.get()):
            self.error_text.config(text="Select MinPts and Eps")
            return

        self.error_text.config(text="")

        filteredKeys = []
        selectedKeys = []

        i = 0

        while i < len(self.boxes):
            if self.boxes[i].get() == 0:
                filteredKeys.append(self.attributes[i])
            else:
                selectedKeys.append(self.attributes[i])
            i += 1


        pre = preprocessing.Preprocessing(self.data)
        #pre.removeAttributes(["Att1", "Att3", "For example"])
        normalized_data = pre.normalizeData()

        clustered_data = None
        k_means = kMeans()
        dbscan = DBSCAN()

        if self.algorithm.get() == 'kmeans':
            clustered_data = k_means.cluster(normalized_data,
                k=self.k_entry.get(),
                dist=self.dist.get(),
                centreMethod='rand',
                filterKeys=filteredKeys)

        else:
            clustered_data = dbscan.cluster(normalized_data,
                eps=float(self.eps_entry.get()),
                MinPts=int(self.min_pts_entry.get()),
                dist=self.dist.get(),
                filterKeys=filteredKeys)
            # data = dbscanner.cluster(normalizedData, 0.065, 4, 'eucl', ['Case', 'class', 'sepal_width', 'sepal_length'])


        with open(self.algorithm.get()+".csv", "w") as outfile:
            keysExist = False
            csvwriter = csv.writer(outfile)
            for line in clustered_data:
                keys = []
                values = []
                for key, value in line.items():
                    keys.append(key)
                    values.append(value)
                if not keysExist:
                    csvwriter.writerow(keys)
                    keysExist = True
                csvwriter.writerow(values)

            # Create imagefile and show image in UI
            imagefile = self.algorithm.get()
            clustWriter = ClusterImageWriter(imagefile)
            if self.algorithm.get() == 'kmeans':
                finalname = clustWriter.writeKMeansImages(
                    k_means.iterData, 
                    k_means.iterCentres,
                    'cluster',
                    'dist2clu',
                    selectedKeys[0], selectedKeys[1])
                clustWriter.writeGif()
            else:
                clustWriter.writeDBSCANImage(clustered_data, 'cluster', selectedKeys[0], selectedKeys[1], 4, 0.07)
            # writer.writeKMeansImages(k_means.iterData, k_means.iterCentres, 'cluster', 'dist2clu', 'petal_width', 'petal_length')
            # img = ImageTk.PhotoImage(Image.open(finalname))
            # self.image_frame.image = img

root = Tk()
gui = ClusterGUI(root)
root.mainloop()
