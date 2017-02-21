from nltk import tokenize
import word2vec
import os


def create_word_vector_phrases(vec_doc):
    word2vec.word2phrase(vec_doc, vec_doc[:len(vec_doc)-4]+"_phrases", verbose=True)


def create_word_vector(vec_doc, vec_bin):
    word2vec.word2vec(vec_doc, vec_bin, size=200, verbose=True)


# Tokenizes and builds the vector models given a directory's path
def build_vector_models(directory, parent):
    files_in_directory = os.listdir(directory)
    # TOKENIZE ------------------------------------------------------------------------------------------
    # makes the /<directory>/t directory
    # if not os.path.exists(parent + '/t'):
    #     os.makedirs(parent +'/t')
    # # go through each file in the directory
    # for f in files_in_directory:
    #     if f.startswith('.'):
    #         continue
    #     tokenize_doc(open(directory+"/"+f, 'r'), open(parent+"/t/"+f, 'w'))
    # Word2Vec ------------------------------------------------------------------------------------------
    # makes the /<directory>/vectors directory
    files_in_token_directory = os.listdir(parent+"/t")
    if not os.path.exists(parent+"/v"):
        os.makedirs(parent+"/v")
    # go through each file in the directory
    for f in files_in_token_directory:
        if f.startswith('.'):
            continue
        create_word_vector_phrases(parent+'/t/'+f)
        create_word_vector(parent+"/t/"+f[:len(f)-4]+"_phrases", parent+"/v/"+f[:len(f)-4]+".bin")


if __name__ == '__main__':
    build_vector_models("/Users/tshaban/Development/honors/data", "/Users/tshaban/Development/honors")