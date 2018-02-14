__author__ = 'amendrashrestha'

import re
import os
import gensim
import nltk
import string

import utilities.IOProperties as prop

def cleanText(post):
    post = post.text
    tag_re = re.compile(r'(<!--.*?-->|<[^>]*>)')
    post = tag_re.sub('', post)
    post = post.replace("\n", " ").strip()
    post = post.replace("\r", " ").strip()
    post = post.replace("\t", " ").strip()
    return post

def validateYMDDate(date):
    mat = re.match('(\d{4})[/.-](\d{2})[/.-](\d{2})$', date)
    if mat is not None:
        return date
    else:
        return

def replace_swedish_month(date):
    if 'Januari' in date:
        return date.replace("Januari", "January")
    elif 'Februari' in date:
        return date.replace("Februari", "February")
    elif 'Mars' in date:
        return date.replace("Mars", "March")
    elif 'Maj' in date:
        return date.replace("Maj", "May")
    elif 'Juni' in date:
        return date.replace("Juni", "June")
    elif 'Juli' in date:
        return date.replace("Juli", "July")
    elif 'Augusti' in date:
        return date.replace("Augusti", "August")
    elif 'Oktober' in date:
        return date.replace("Oktober", "October")
    else:
        return date

def replace_swedish_mon(date):
    if 'Okt' in date:
        return date.replace("Okt", "Oct")
    elif 'Maj' in date:
        return date.replace("Maj", "May")
    else:
        return date

def write_news_link(topic_url, filepath):
    with open(filepath, "a") as text_file:
        text_file.write(topic_url)
        text_file.write("\n")

def read_topic(text):
    with open(text) as content:
        topic_id = content.readlines()
        return topic_id

def read_text_file(filepath):
    with open(filepath) as content:
        topic_url = content.readlines()
        return topic_url


def write_text(text, filepath):
    with open(filepath, "a") as content:
        content.write(text)
        content.write("\n")

def write_tsv(text, filepath):
    with open(filepath, "a") as content:
        content.write(text)
        content.write("\n")

def write_tuple(post_info, filepath):
    with open(filepath, "a", encoding='utf-8') as text_file:
        text_file.write(''.join('%s \t %s \n' % x for x in post_info))

def write_list(post_info, filepath):
    with open(filepath, "a", encoding='utf-8') as text_file:
        for number, item in post_info:
            text_file.write(str(item))
            text_file.write("\t")
        text_file.write("\n")


def save_word2vec_format(fname, model, top=100):
    with gensim.utils.smart_open(fname, 'wb') as fout:
        fout.write(gensim.utils.to_utf8("%s %s\n" % (top, 100)))
        # store in sorted order: most frequent words at the top
        for word, vocab in sorted(model.vocab.items(), key=lambda item: -item[1].count)[:top]:
            row = model.syn0[vocab.index]
            fout.write(gensim.utils.to_utf8("%s %s\n" % (word, ' '.join("%f" % val for val in row))))

def get_full_path(path):
    return os.path.join(prop.ROOT_FOLDER_PATH, path)

def filter_text(text):
    table = str.maketrans({key: None for key in string.punctuation})
    text = text.translate(table)
    text = remove_verb(text)

    return text

def remove_verb(text):
    verb_list = [word.strip() for word in read_text_file(prop.verb_filepath)]
    text = [word for word in nltk.word_tokenize(text) if word not in verb_list]

    return text