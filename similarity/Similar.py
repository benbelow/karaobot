
import gensim.models.keyedvectors as word2vec
from gensim import utils, matutils
import os


cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory

trained_path = "./data/source_data/GoogleNews-vectors-negative300.bin"
model = word2vec.KeyedVectors.load_word2vec_format(trained_path, binary=True)

def most_similar(pos, neg, topn):
    return model.most_similar_cosmul(pos, neg, topn)
