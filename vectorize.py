import word2vec
from magicutil import files_in_directory


def build_vector_model(file_name, parent_directory):
    # Build word vector phrases
    word2vec.word2phrase(parent_directory + "/tokens/" + file_name,
                         parent_directory + "/phrases/" + file_name, verbose=True)

    # Build the word vector now
    word2vec.word2vec(parent_directory + "/phrases/" + file_name, parent_directory + "/vectors/" + file_name,
                      size=200, verbose=True)


def vector_models_all_files(parent_directory):
    # get a list of all the files in the directory ---------------------------------------------
    files = files_in_directory(parent_directory + "/tokens/", short=True)

    # go through each file and build a vector model for each ---------------------------------------------
    for f in files:
        build_vector_model(f, parent_directory)
