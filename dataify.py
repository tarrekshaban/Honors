from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
from magicutil import files_in_directory
import pickle
import numpy as np
import os
import time


def boring_tokenizer(text):
    return text.split()

start = time.time()
# Builds our Tfidf model ----------------------------------------------------------------
tf = TfidfVectorizer(input='filename', decode_error='ignore', strip_accents='ascii',
                     stop_words='english', ngram_range=(1, 3), tokenizer=boring_tokenizer)

tfidf_matrix =  tf.fit_transform(files_in_directory("/Users/tshaban/Desktop/tokens"))

pickle.dump(tf, open('tf.p', 'wb'))
pickle.dump(score, open('score.p', 'wb'))

feature_names = tf.get_feature_names()

len(feature_names)
print time.time() - start