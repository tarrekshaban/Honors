import word2vec
import os
from magicutil import files_in_directory
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool


class Vectorize(object):

    def __init__(self, token_dir, phrase_dir, vector_dir):
        self.token_dir = token_dir
        self.phrase_dir = phrase_dir
        self.vector_dir = vector_dir

        if not os.path.exists(self.token_dir):
            raise IOError(self.token_dir + " is not a directory or does not exist.")

        # if parent_directory/phrases does not exist, make it
        if not os.path.exists(self.phrase_dir):
            os.makedirs(self.phrase_dir)

        # if parent_directory/vectors does not exist, make it
        if not os.path.exists(self.vector_dir):
            os.makedirs(self.vector_dir)

    def build_vector_model(self, file_name, verbose=True, size=200):
        # Build word vector phrase models
        word2vec.word2phrase(self.token_dir + "/" + file_name,
                             self.phrase_dir + "/" + file_name,
                             verbose=verbose)

        # Build the word vector now
        word2vec.word2vec(self.phrase_dir + "/" + file_name,
                          self.vector_dir + "/" + file_name + ".bin",
                          size=size, verbose=verbose)

    def vector_models_all_files(self, threaded=False, num_threads=4):
        # get a list of all the files in the directory
        files = files_in_directory(self.token_dir, short=True)

        # go through each file and build a vector model for each
        if threaded:
            pool = ThreadPool(num_threads)
            # a threaded approach
            pool.map(self.build_vector_model, files)

            pool.close()
            pool.join()
        else:
            for f in files:
                self.build_vector_model(f)

