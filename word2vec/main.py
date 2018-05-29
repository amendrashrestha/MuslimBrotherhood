import os, sys

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(APP_ROOT)

import utilities.controller as cont

def init_assoc_measure():
    cont.assoc_measure()

def init_word2vec_measure():
    cont.word2vec_measure()

def init_measure_count():
    cont.measure_count()

def init_return_sentences():
    cont.writeOrganizationSentences()

if __name__ == "__main__":
    # init_assoc_measure()
    # init_word2vec_measure()
    init_measure_count()
    # init_return_sentences()