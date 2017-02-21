from collections import Counter
from nltk import tokenize
from nltk.corpus import stopwords
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
            # if the word is a stop word or another form of prohibited word
            if not is_allowed(word):
                return -1
            # word is not a prohibited word... thus we can add it to our dictionary
            self.vocab[word] = [0 for x in range(0, self.count)]
        f_id = self.lookup_document_id(file_name)
        if self.vocab[word][f_id] is 0:
            self.vocab[word][f_id] = 1
        return 0

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

    def vocab_list_idf(self):
        vocab_list = dict()
        for word, val in self.vocab.iteritems():
            vocab_list[word] = float(math.log((self.number_of_documents()) /
                                           (float(self.number_of_documents_contain_word(word)))))
        return vocab_list


# Calculates the TF-IDF score for all files in a directory
# Each file must have one TWEET per line
def calculate_tfid(directory, itter_flag=True, clean_files=True, will_tokenize=True):
    documents = list()
    files = os.listdir(directory)
    mapper = Mapper()

    # Adds all files to the mapper
    for f in files:
        if not f.startswith('.'):
            mapper.add_document(f)

    if clean_files:
        for f in files:
            if not f.startswith('.'):
                time1 = time.time()
                f_new = open(directory + "/" + f + "_clean", 'w')
                count = 0
                for tweet in open(directory + "/" + f, 'r'):
                    try:
                        f_new.write(tweet.decode('utf8').encode('utf8'))
                    except UnicodeDecodeError:
                        count += 1
                        continue
                    except UnicodeEncodeError:
                        count += 1
                        continue
                print "Convert 1: " + str(time.time() - time1) + "; Count: " + str(count)

    # Goes through each document building Counters and doing other magic
    for f in files:
        # Avoids reading any of the .DS files on macOS
        if not f.startswith('.'):
            s = time.time()
            print f
            # Creates a Counter() for documents vocab
            c = Counter()

            if will_tokenize:
                # If the user WANTS to tokenize the documents as well as TF-IDF
                if itter_flag:
                    # Add the tokenized version of each tweet to the counter
                    for tweet in open(directory + "/" + f + "_clean", 'r'):
                        tweet = tweet.lower()  # lowercase the tweet BEFORE tokenizing it
                        try:
                            c.update(tokenize.word_tokenize(tweet.decode('utf8')))
                        except UnicodeDecodeError:
                            continue
                else:
                    try:
                        c.update(tokenize.word_tokenize(open(directory + "/" + f, 'r').read().decode('utf8').lower()))
                    except UnicodeDecodeError:
                        continue
            else:
                # If the user ALREADY HAS tokenized documents and is only interested in TF-IDF
                for tweet in open(directory + "/" + f, 'r'):
                    try:
                        tweet = tweet.decode('utf8').lower()
                        scratch = tweet.split()
                        c.update(scratch)
                    except UnicodeDecodeError:
                        continue

            print "time: " + str(time.time() - s)
            # Adds all words encountered in the tweets to the mapper
            stack = []
            num_words = 0
            for key, value in c.iteritems():
                r = mapper.add_word(key, f)
                if r == -1:
                    stack.append(key)
                else:
                    num_words += value
            for key in stack:
                del c[key]

            # Add the counter and the label to the documents list
            documents.append((f, num_words, copy.copy(c)))

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

    # Save the TFIDF matrix as a pickle file
    pickle.dump(tfidf_matrix, open('./tfidf_score.p', 'wb'))

if __name__ == '__main__':
    calculate_tfid("/Users/tshaban/Development/honors/data", itter_flag=False, clean_files=True)