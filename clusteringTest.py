
from clustering.kMeans import kMeans
from clustering.DBSCAN import DBSCAN
import preprocessing
import pprint
import csv

def main():
    with open("iris.csv", 'r') as datafile:
        reader = csv.DictReader(datafile, delimiter=';')
        data = []
        for line in reader:
            data.append(line)

        pre = preprocessing.Preprocessing(data)
        normalized_data = pre.normalizeData()

        k_means = kMeans()
        data_kmeans = k_means.cluster(normalized_data, k=3, dist='eucl', centreMethod='rand', filterKeys=['Case', 'class'])
        
        dbscan = DBSCAN()
        data_dbscan = dbscan.cluster(normalized_data, eps=0.3, MinPts=2, dist='eucl', filterKeys=['Case', 'class'])

        #printData(data_dbscan)
        printData(data_kmeans)

        pp = pprint.PrettyPrinter(indent=2)
        #pp.pprint(data_kmeans)
        #pp.pprint(data_dbscan)
        
        # Cluster centres and clustered data listed in every iteration:
        #pp.pprint(k_means.iterCentres)
        #pp.pprint(k_means.iterData)


def printData(d):
    print()
    for i, case in enumerate(d):
        if i > 0:
            if d[i-1]['cluster'] != case['cluster']:
                print()
        print('%5d: %s' % (i, case['cluster']))
    print()

if __name__ == "__main__":
    main()