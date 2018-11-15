#!/usr/bin/env python3

# from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import *
import clustering

def main():
    # window = Tk()
    # textBox=Text(window, height=2, width=10)
    # textBox.pack()
    # buttonCommit=Button(window, height=1, width=10, text="Commit", 
    #                     command=lambda: retrieve_input())
    # buttonCommit.pack()
    filename = askopenfilename()

    c = clustering.Clustering()
    c.cluster_Kmeans([{"avain": "arvo"}, {"avain": "arvo2"}], k=2)

    print(filename)

# if __name__ == "__main()__":
#     main()
main()


# clusterien määrä
# 