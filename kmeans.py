from gensim.models import word2vec
from tfidf import build_doc_tf_idf_list
import numpy as np
from scipy import spatial
from collections import Counter

# Cosine similarity
def cos_sim(v, w):
    return 1 - spatial.distance.cosine(v, w)


# Load a vector representation of the document using gensim
# Vector was not created with gensim however
def load_model(document):
    return word2vec.Word2Vec.load_word2vec_format(document, binary=True, unicode_errors='ignore')


# Load a list() which contains every word in the document, sorted by TF-IDF score
# Use for the K-Means algorithm
def load_doc_df_idf(document):
    return build_doc_tf_idf_list(document)


# The vector data type should be an object with the following
def init_centroids(k, vectors, model):
    centroids = list()
    # append Numpy representations of the top k vectors by TF-IDF
    for c in vectors[0:k]:
        centroids.append(np.copy(model[c[0]]))
    return centroids


# Finds the new centroid
def find_centroid(cluster, model):
    centroid = np.copy(model[cluster[0][0]])
    for c in cluster[1:]:
        centroid += model[c[0]]
    n = 1.0 / len(cluster)
    centroid *= n
    return centroid


# K-Means clustering alogrithm
def kmeans_clustering(k, document, threshold=0.99):
    # Init everything for K-Means clustering ------------------------------------------------
    vectors = build_doc_tf_idf_list(document, threshold=200)
    model = load_model("/Users/tshaban/Desktop/t/vectors/10-08-2016_2_PM.bin")  # Need to change this document
    model.init_sims(replace=True)
    centroids = init_centroids(k, vectors, model)  # these centroids are Numpy Arrays

    # Iterate at most 50 times, MAX
    for iter in xrange(50):
        # define K clusters ------------------------------------------------
        clusters = [[] for _ in xrange(k)]

        # maximization ------------------------------------------------
        for vector in vectors:
            if vector[0] in model:
                m = max([(cos_sim(model[vector[0]], centroid), i) for (i, centroid) in enumerate(centroids)])
                clusters[m[1]].append(vector)

        # expectation
        new_centroids = [find_centroid(cluster, model) for cluster in clusters]
        m = min([cos_sim(centroids[i], new_centroids[i]) for i in xrange(k)])
        print m
        if m > threshold:
            break
        centroids = new_centroids
        print iter
    return clusters


if __name__ == '__main__':
    K = 10
    clusters = kmeans_clustering(K, "/Users/tshaban/Desktop/tf_idf_score.txt")
    for i in range(K):
        print str(i) + " -------------------"
        clusters[i].sort(key=lambda tup: tup[1], reverse=True)
        print [w[0] for w in clusters[i][0:20]]
