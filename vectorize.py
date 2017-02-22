import word2vec
import os
from magicutil import files_in_directory


def build_vector_model(file_name, token_dir, phrase_dir, vector_dir):
    if not os.path.exists(token_dir) or :
        raise IOError(token_dir + " is not a directory or does not exist.")
    # if parent_directory/phrases does not exist, make it ---------------------------------------------
    if not os.path.exists(phrase_dir):
        os.makedirs(phrase_dir)
    # if parent_directory/vectors does not exist, make it ---------------------------------------------
    if not os.path.exists(vector_dir):
        os.makedirs(vector_dir)

    # Build word vector phrases
    word2vec.word2phrase(parent_directory + "/tokens/" + file_name,
                         parent_directory + "/phrases/" + file_name,
                         verbose=True)

    # Build the word vector now
    word2vec.word2vec(parent_directory + "/phrases/" + file_name,
                      parent_directory + "/vectors/" + file_name[0:len(file_name)-4] + ".bin",
                      size=200, verbose=True)


def vector_models_all_files(parent_directory):
    # get a list of all the files in the directory ---------------------------------------------
    files = files_in_directory(parent_directory + "/tokens", short=True)

    # go through each file and build a vector model for each ---------------------------------------------
    for f in files:
        build_vector_model(f, parent_directory)


if __name__ == '__main__':
    vector_models_all_files("/Users/tshaban/Desktop/data")