import os
import sys

ROOT_FOLDER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# print(ROOT_FOLDER_PATH)
# MAIN_DIRECTORY = (os.path.dirname(__file__))

# svd_url_filepath = os.path.join(ROOT_FOLDER_PATH, '/files/url/svd_article_url.txt')
svd_url_filepath = os.path.expanduser('~') + '/repo/Crawler/files/url/svd_article_url.txt'

dn_url_filepath = os.path.expanduser('~') + '/repo/Crawler/files/url/dn_article_url.txt'
verb_filepath = os.path.expanduser('~') + '/repo/Crawler/files/word/verb.txt'


graph = os.path.expanduser('~') + '/repo/Crawler/files/graph/'
date_count = os.path.expanduser('~') + '/repo/Crawler/files/count/'
word2vec_count = os.path.expanduser('~') + '/repo/Crawler/files/word2vec/'