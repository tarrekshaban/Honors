from gensim.models import word2vec
from tfidf import build_doc_tf_idf_list
import numpy as np
from scipy import spatial
import cPickle as pickle


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
    return build_doc_tf_idf_list(document, threshold=1000)


# A custom built K-Means clustering Algorithm for our purposes
class KmeansClustering(object):
    def __init__(self, vector_document):
        self.model = load_model(vector_document)
        self.model.init_sims(replace=True)

        # These properties are only available after running the clustering algorithm -----------------------------------
        self.centroids = None
        self.clusters = None
        self.file = None

    def cluster(self, k, document, threshold=0.99, max_itterations=50):
        self.file = document
        vectors = build_doc_tf_idf_list(document)
        centroids = self._init_centroids(k, vectors)

        for iter in xrange(max_itterations):
            # create k clusters ----------------------------------------------------------------------------------------
            clusters = [[] for _ in xrange(k)]

            # perform maximization step here ---------------------------------------------------------------------------
            for vector in vectors:
                if vector[0] in self.model:
                    m = max([(cos_sim(self.model[vector[0]], centroid), i) for (i, centroid) in enumerate(centroids)])
                    clusters[m[1]].append(vector)

            # expectation ----------------------------------------------------------------------------------------------
            new_centroids = list()
            for i, cluster in enumerate(clusters):
                if len(cluster) > 0:
                    new_centroids.append(self._find_centroid(cluster))
                else:
                    print len(centroids), i
                    new_centroids.append(centroids[i])

            m = min([cos_sim(centroids[i], new_centroids[i]) for i in xrange(k)])

            if m > threshold:
                break

            # new centroids --------------------------------------------------------------------------------------------
            centroids = new_centroids

        # Remember centroids and the clusters
        self.centroids = centroids
        self.clusters = clusters

    def extract_important_values_tfidf(self, num=15):
        important = [None for _ in range(len(self.clusters))]

        for iv in range(len(self.clusters)):
            self.clusters[iv].sort(key=lambda tup: tup[1], reverse=True)
            important[iv] = [w[0] for w in self.clusters[iv][0:num]]

        return important

    def extract_important_values_centrality(self, num=15):
        top_scores = list()

        for i, cluster in enumerate(self.clusters):
            cluster_top = list()
            for vector in cluster:
                # tup of (score, word)
                cluster_top.append((cos_sim(self.model[vector[0]], self.centroids[i]), vector[0]))
            # sort the best and throw away the rest
            cluster_top.sort(key=lambda tup: tup[0], reverse=True)
            top_scores.append(cluster_top[0:num])

        return top_scores

    def extract_dense_vector(self, top=300):
        dense = list()
        labels = list()

        # for each cluster
        for i, c in enumerate(self.clusters):
            # for each vector in the cluster
            count = 0
            for vector in c:
                if count >= top:
                    break
                if vector[0] in self.model:
                    # add label to list of labels
                    labels.append((vector[0], i))
                    # add numpy array (1 X N) | N is # of features
                    dense.append(self.model[vector[0]])

        nump = np.concatenate(dense)
        return nump, labels

    def _init_centroids(self, k, vectors):
        centroids = list()
        # append Numpy representations of the top k vectors by TF-IDF
        for c in vectors[:k]:
            if c[0] in self.model:
                centroids.append(np.copy(self.model[c[0]]))
        # print top 50 vectors
        for c in vectors[:50]:
            print c
        return centroids

    def _find_centroid(self, cluster):
        centroid = np.copy(self.model[cluster[0][0]])
        for c in cluster[1:]:
            if c[0] in self.model:
                centroid += self.model[c[0]]
        n = 1.0 / len(cluster)
        centroid *= n
        return centroid


def save(file_path, k_object):
    pickle.dump(k_object, open(file_path, 'wb'))


def load(file_path):
    return pickle.load(open(file_path, 'rb'))
