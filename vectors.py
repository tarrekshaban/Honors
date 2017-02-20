from nltk import tokenize
import word2vec
import os


# Tokenize the give document: doc
# Ignores tweets that throw a UnicodeEncodeError to not taint the corpus with partially encoded tweets
def tokenize_doc(doc_fd, new_fd):
    for line in doc_fd:
        # Actually tokenize the strings here
        try:
            new_fd.write(" ".join(tokenize.word_tokenize(line.decode("ascii", 'ignore')))+"\n")
        except UnicodeDecodeError:
            print "UnicodeDecodeError: " + line
        except UnicodeEncodeError:
            print "UnicodeEncodeError: " + line


def create_word_vector_phrases(vec_doc):
    word2vec.word2phrase(vec_doc, vec_doc+"_phrases", verbose=True)


def create_word_vector(vec_doc, vec_bin):
    word2vec.word2vec(vec_doc, vec_bin, size=200, verbose=True)


# Tokenizes and builds the vector models given a directory's path
def build_vector_models(directory, parent):
    files_in_directory = os.listdir(directory)
    # TOKENIZE ------------------------------------------------------------------------------------------
    makes the /<directory>/t directory
    if not os.path.exists(parent+ '/t'):
        os.makedirs(parent+'/t')
    # go through each file in the directory
    for f in files_in_directory:
        tokenize_doc(open(directory+"/"+f, 'r'), open(parent+"/t/"+f[:len(f)-4], 'w'))
    # Word2Vec ------------------------------------------------------------------------------------------
    # makes the /<directory>/vectors directory
    files_in_token_directory = os.listdir(parent+"/t")
    if not os.path.exists(parent+"/v"):
        os.makedirs(parent+"/v")
    # go through each file in the directory
    for f in files_in_token_directory:
        if f == ".DS_S": continue
        create_word_vector_phrases(parent+'/t/'+f)
        create_word_vector(parent+"/t/"+f+"_phrases", parent+"/v/"+f+".bin")


if __name__ == '__main__':
    build_vector_models("/Users/tshaban/Development/honors/data", "/Users/tshaban/Development/honors")