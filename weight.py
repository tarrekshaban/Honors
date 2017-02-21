from collections import Counter
from nltk.corpus import stopwords
from magicutil import files_in_directory
import os
import time
import math
import copy
import cPickle as pickle


# Process Stop Words and other things
# RULES: No Stop Words; No Punctuation
def is_allowed(word):
    if word in stopwords.words('english'):
        return False
    if word in [".", "!", ",", "/", "?", ":", "https", "https:", "'", "&", "rt", "@", "``", "@", "-", "#", "'s",
                "''", ";", "...", "''", "'re", "amp", "n't", "(", ")", "\u2026"]:
        return False
    if word.startswith("//") or word.startswith("/"):
        return False
    return True


class Mapper(object):
    def __init__(self):
        self.vocab = dict()
        self.mapping = dict()
        self.count = 1  # Note: count should be the same as len(files)

    def add_document(self, file_name):
        if file_name not in self.mapping:
            self.mapping[file_name] = self.count
            self.count += 1

    def lookup_document_id(self, file_name):
        if file_name in self.mapping:
            return self.mapping[file_name]
        else:
            return -1

    def add_word(self, word, file_name):

        if word not in self.vocab:
            # word has not been seen before...
            self.vocab[word] = [0 for x in range(0, self.count)]
        f_id = self.lookup_document_id(file_name)

        # Set the word to be present
        if self.vocab[word][f_id] is 0:
            self.vocab[word][f_id] = 1

    def number_of_documents(self):
        return float(self.count)

    # Returns -1    if the word has not been seen yet
    # Returns f_id  if it has been seen
    def number_of_documents_contain_word(self, word):
        if word not in self.vocab:
            return -1
        counter = 0
        for f in self.vocab[word]:
            counter += f
        return float(counter)

    # Determine the IDF score for the vocab
    def vocab_list_idf(self):
        vocab_list = dict()
        for word, val in self.vocab.iteritems():
            vocab_list[word] = float(math.log((self.number_of_documents()) /
                                              (float(self.number_of_documents_contain_word(word)))))
        return vocab_list


# Calculates the TF-IDF score for all files in a directory
# Each file must have one TWEET per line
def calculate_tfid(directory):
    documents = list()
    files = files_in_directory(directory, short=True)
    mapper = Mapper()

    # Adds all files to the mapper
    for f in files:
        mapper.add_document(f)

    # Goes through each document building Counters and doing other magic
    for f in files:
        print f
        c = Counter()
        for tweet in open(directory + "/" + f, 'r'):
            try:
                tweet = tweet.decode('utf8')
                c.update([word for word in tweet.split() if is_allowed(word)])
            except UnicodeDecodeError:
                continue

            num_words = 0
            for key, value in c.iteritems():
                mapper.add_word(key, f)
                num_words += value

            # Add the counter and the label to the documents list
            documents.append((f, num_words, copy.copy(c)))
    print "Made it 3"
    # Build a vocab list of IDF scores
    vocab_list = mapper.vocab_list_idf()
    tfidf_matrix = list()
    for doc in documents:
        doc_list = list()
        for word, val in doc[2].iteritems():
            score = (float(val) / float((doc[1]))) * float(vocab_list[word])
            doc_list.append((word, score))
        doc_list.sort(key=lambda tup: tup[1], reverse=True)
        tfidf_matrix.append((doc[0], copy.copy(doc_list)))

    print "Made it 4"
    # Save the TFIDF matrix as a pickle file
    pickle.dump(tfidf_matrix, open('./tfidf_score.p', 'wb'))

if __name__ == '__main__':
    calculate_tfid("/Users/tshaban/Desktop/tokens")