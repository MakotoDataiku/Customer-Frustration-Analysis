from aspect_clustering.get_word_vectors import get_word_vectors
import dataiku
from sklearn import cluster

NUM_CLUSTERS = dataiku.get_custom_variables()['NUM_CLUSTERS']

def get_word_clusters(unique_aspects, nlp):
    print("Found {} unique aspects for this product".format(len(unique_aspects)))
    asp_vectors = get_word_vectors(unique_aspects, nlp) # gets the word vector for each noun 
    if len(unique_aspects) <= NUM_CLUSTERS:
        print("Too few aspects ({}) found. No clustering required...".format(len(unique_aspects)))
        return list(range(len(unique_aspects)))

    print("Running k-means clustering...")
    n_clusters = NUM_CLUSTERS
    kmeans = cluster.KMeans(n_clusters=n_clusters)
    kmeans.fit(asp_vectors)
    labels = kmeans.labels_
    return labels