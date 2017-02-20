from collections import Counter
from nltk import tokenize
from nltk.corpus import stopwords
import os
import time
import copy


# Process Stop Words and other things
# RULES: No Stop Words; No Punctuation
def is_allowed(word):
    if word in stopwords.words('english'):
        return False
    if word in [".", "!", ",", "/", "?"]:
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
        return self.count

    # Returns -1    if the word has not been seen yet
    # Returns f_id  if it has been seen
    def number_of_documents_contain_word(self, word):
        if word not in self.vocab:
            return -1
        counter = 0
        for f in self.vocab[word]:
            counter += f
        return counter


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
                f_new = open(directory + "/" + f[:len(f)-4] + "", 'w')
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
            print f
            # Creates a Counter() for documents vocab
            c = Counter()

            if will_tokenize:
                # If the user WANTS to tokenize the documents as well as TF-IDF
                if itter_flag:
                    # Add the tokenized version of each tweet to the counter
                    for tweet in open(directory + "/" + f, 'r'):
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

            # Adds all words encountered in the tweets to the mapper
            print len(c)
            stack = []
            num_words = 0
            for key, value in c.iteritems():
                r = mapper.add_word(key, f)
                if r == -1:
                    stack.append(key)
                else:
                    num_words += value
            print len(stack)
            print stack
            for key in stack:
                del c[key]
            print len(c)

            # Add the counter and the label to the documents list
            documents.append((f, num_words, c.copy()))

    # Now going on to calculate the TFIDF score
    D = mapper.number_of_documents() # The number of documents we are dealing with


def bag_of_words(doc, token_doc):
    # open the docs to read from and write to
    doc_fd = open(doc, mode='r')
    token_doc = open(token_doc, mode='w')
    # create a Counter() for document frequency counts
    dfs = Counter()
    # goes through each tweet (line) in the doc that was given
    count = 0
    for tweet in doc_fd:
        # Tokenize the tweet
        try:
            tokens = tokenize.word_tokenize(tweet.decode('utf8'))
        except UnicodeDecodeError:
            continue
        # write the tokenized strings to a text file for vectorization
        s = " ".join(tokens)
        token_doc.write(s.encode("utf8", 'ignore')+"\n")
        # filter out the stop words
        filtered = [w.lower() for w in tokens if is_allowed(w)]
        dfs.update(filtered)
        print count
        count += 1
    return dfs


def run_bow(parent):
    data_dir = parent + "/data"  # Date Directory
    t_dir = parent + "/t"  # Token Directory
    # Create token directory if it does not exists already
    if not os.path.exists(parent + "/t"):
        os.makedirs(parent + "/t")
    # List all files in the data directory to be processed
    files_in_directory = os.listdir(data_dir)
    bow_vectors = list()
    for doc in files_in_directory:
        # Appends tuple (doc name, Counter()) to the bag of words vector
        bow_vectors.append((doc, bag_of_words(data_dir + "/" + doc, t_dir + "/" + doc)))
    return bow_vectors


def document_score(bow_vectors):
    D = float(len(bow_vectors))  # Number of documents read in by the algorithm

calculate_tfid("/Users/tshaban/Development/honors/data", itter_flag=False, clean_files=False)