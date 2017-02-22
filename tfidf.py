import math
from collections import Counter
from magicutil import files_in_directory
from nltk.corpus import stopwords


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
            # document is in the mapping
            return self.mapping[file_name]
        else:
            # document is not in the mapping
            return -1

    def add_word(self, word, file_name):
        if word not in self.vocab:
            # the word has not been seen before
            self.vocab[word] = [0 for x in range(0, self.count)]
        f_id = self.lookup_document_id(file_name)
        # Set the word to be present
        if self.vocab[word][f_id] is 0:
            self.vocab[word][f_id] = 1

    def number_of_documents(self):
        return float(self.count)

    def number_of_documents_contain_word(self, word):
        if word not in self.vocab:
            return -1
        counter = 0
        for f in self.vocab[word]:
            counter += f
        return float(counter)


def is_prohibited(word):
    s = {'.', ':', '...', ',', "'s", '``', 'RT', '!', '?', '&', "n't", '-', "`", 'https', '--'}
    if word in s:
        return True
    else:
        return False


def calculate_idf(directory, file_path):
    files = files_in_directory(directory, short=True)
    fd_write = open(file_path, 'w')
    mapper = Mapper()
    english_stops = set(stopwords.words('english'))

    # add all files to the mapper --------------------------------------
    for f in files:
        mapper.add_document(f)

    # add all words to the mapper per file --------------------------------------
    for f in files:
        print f
        for line in open(directory + "/" + f, 'r'):
            try:
                for word in line.decode('utf8').split():
                    if word not in english_stops and not word.startswith("https://") and not is_prohibited(word) \
                            and not word.startswith("@"):
                        mapper.add_word(word, f)
            except UnicodeDecodeError:
                continue

    # calculates idf score for each word --------------------------------------
    print "started ------"
    for key, value in mapper.vocab.iteritems():
        num = mapper.number_of_documents_contain_word(key)
        calc = mapper.number_of_documents()/num
        try:
            fd_write.write(key.encode('utf8') + "\t" + str(mapper.number_of_documents()) + "\t" + str(num)
                                                + "\t" + str(calc) + "\t" + str(math.log(calc)) + "\n")
        except UnicodeEncodeError:
            continue
    print "finished ------"


def calculate_tf_idf(file_path, idf_dict, new_file_path):
    fd_file = open(file_path, 'r')
    new_file = open(new_file_path, 'w')
    c = Counter()

    # for each tweet in the file, add words to dictionary --------------------------------------
    for line in fd_file:
        try:
            c.update(line.decode('utf8').split())
        except UnicodeDecodeError:
            continue
    # find the number of words in the document --------------------------------------
    num_words = 0
    for key, value in c.iteritems():
        # as long as the word is in idf we know that it is not a stop word
        if key in idf_dict:
            num_words += value

    # finally print out the thing --------------------------------------
    for key, value in c.iteritems():
        if key in idf_dict:
            try:
                df = float(value) / float(num_words)
                idf = float(idf_dict[key][0])
                log_idf = float(idf_dict[key][1])

                # WORD \t numberOfWords \t countOfWord \t df \t idf \t log idf
                new_file.write(key.encode('utf8') + "\t" + str(num_words) + "\t" + str(value) + "\t"
                               + str(df) + "\t" + str(df * idf) + "\t" + str(df * log_idf) + "\n")
            except UnicodeEncodeError:
                continue

    new_file.close()


def build_idf_dic(file_path):
    fd_idf = open(file_path, 'r')
    idf_dict = dict()

    for line in fd_idf:
        try:
            args = line.decode('utf8').split("\t")
            idf_dict[args[0]] = (float(args[3]), float(args[4]))
        except UnicodeDecodeError:
            continue

    return idf_dict


def build_doc_tf_idf_list(file_path, threshold=1):
    fd_score = open(file_path, 'r')
    tf_idf_list = list()

    for line in fd_score:
        try:
            args = line.decode('utf8').split("\t")
            if float(args[2] > threshold):
                tf_idf_list.append((args[0], float(args[4]), float(args[5])))
        except UnicodeDecodeError:
            continue

    tf_idf_list.sort(key=lambda tup: tup[1], reverse=True)

    return tf_idf_list


if __name__ == '__main__':
    calculate_idf("/Users/tshaban/Desktop/data/tokens", "/Users/tshaban/Desktop/data/idf_values.txt")
    # build_idf_dic("/Users/tshaban/Desktop/tfidf.txt")
    # calculate_tf_idf("/Users/tshaban/Desktop/tokens/10-08-2016_2_PM.txt",
    #                   build_idf_dic("/Users/tshaban/Desktop/tfidf.txt"), "/Users/tshaban/Desktop/tf_idf_score.txt")
    # build_doc_tf_idf_list("/Users/tshaban/Desktop/tf_idf_score.txt")