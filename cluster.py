from nltk import tokenize


# Tokenize the give document: doc
def tokenize_doc(doc_fd, new_fd):
    for line in doc_fd:
        new_fd.write(" ".join(tokenize.word_tokenize(line)))

fd = open("/Users/tshaban/Development/honors/data/10-09-2016_0.txt", 'r')
new_fd = open("/Users/tshaban/Development/honors/data/test.txt", 'w')
tokenize_doc(fd, new_fd)