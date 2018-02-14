import model.dbScript as db

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.collocations import BigramCollocationFinder

from gensim.models import Phrases
from gensim.models import Word2Vec
from nltk.corpus import stopwords

import utilities.IOReadWrite as IO
import utilities.IOProperties as prop

bigram_measures = nltk.collocations.BigramAssocMeasures()

def init_assoc_measure():

    text = ""
    articles = db.get_articles()

    for single_article in articles:
        text += ''.join(single_article.lower())

    tokenizer = RegexpTokenizer(r'\w+')

    word_token = tokenizer.tokenize(text)

    finder = BigramCollocationFinder.from_words(word_token, window_size=10)

    # scored = finder.score_ngrams(bigram_measures.likelihood_ratio)
    #
    # # Group bigrams by first word in bigram.
    # prefix_keys = collections.defaultdict(list)
    # for key, scores in scored:
    #     prefix_keys[key[0]].append((key[1], scores))
    #
    # # Sort keyed bigrams by strongest association.
    # for key in prefix_keys:
    #     prefix_keys[key].sort(key=lambda x: -x[1])
    #
    # print('muslimska', prefix_keys['muslimska'][:5])


    finder.apply_freq_filter(100)
    # print(finder.score_ngrams(bigram_measures.pmi))
    res = finder.nbest(bigram_measures.pmi, 100)
    # print(finder.score_ngrams(bigram_measures.pmi))

    for k in res:
        print(k)

def init_word2vec_measure():

    article_names = ["expressen", "aftonbladet", "svd","dn"] #,
    sentences = []

    for single_article in article_names:

        print(" \n *** " +single_article+ " *****")
        articles = db.get_articles(single_article)
        bigram = Phrases()

        for row in articles:
            row = IO.filter_text(row.lower())
            sentence = [word
                        for word in row
                        if word not in stopwords.words('swedish')
                        ]

            sentences.append(sentence)
            bigram.add_vocab([sentence])

    print(len(sentences))

    num_features = 300    # Word vector dimensionality
    min_word_count = 5   # Minimum word count
    num_workers = 8       # Number of threads to run in parallel
    context = 5           # `context window` is the maximum distance between the current and predicted word within a sentence.
    downsampling = 1e-3   # Downsample setting for frequent words

    # bigram_model = Word2Vec(bigram[sentences], size=100)
    bigram_model = Word2Vec(bigram[sentences], workers=num_workers, \
            size=num_features, sg=1, min_count = min_word_count, \
            window = context, sample = downsampling)

    word2vec_result = bigram_model.most_similar(positive=['muslimska_brödraskapet'], topn=200)
    # filepath = prop.word2vec_count+single_article+".tsv"
    filepath = prop.word2vec_count+"all_10.tsv"

    IO.write_tuple(word2vec_result, filepath)


if __name__ == "__main__":
    # init_assoc_measure()
    init_word2vec_measure()