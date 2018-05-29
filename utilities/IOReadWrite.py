__author__ = 'amendrashrestha'

import re
import os
import gensim
import nltk
import string
import traceback
import glob2
import codecs

import numpy as np

import utilities.IOProperties as prop

def cleanText(post):
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

def write_single_list(post_info, filepath):
    with open(filepath, "a", encoding='utf-8') as text_file:
        for item in post_info:
            text_file.write(item+"\n")

def save_word2vec_format(fname, model, top=100):
    with gensim.utils.smart_open(fname, 'wb') as fout:
        fout.write(gensim.utils.to_utf8("%s %s\n" % (top, 100)))
        # store in sorted order: most frequent words at the top
        for word, vocab in sorted(model.vocab.items(), key=lambda item: -item[1].count)[:top]:
            row = model.syn0[vocab.index]
            fout.write(gensim.utils.to_utf8("%s %s\n" % (word, ' '.join("%f" % val for val in row))))

def get_full_path(path):
    return os.path.join(prop.ROOT_FOLDER_PATH, path)

def get_document_filenames(document_path):
    # print(document_path)
    files = [file for file in glob2.glob(document_path + '*.txt', recursive=True)]
    return files

def create_file_with_header(filepath, features):
    with open(filepath, 'a') as outtsv:
        features = '\t'.join(features)
        outtsv.write(features)
        outtsv.write("\n")

def return_words_frequency(filepath):
    with codecs.open(filepath, 'r', encoding="utf-8") as f:
        functions = [x.lower().strip() for x in f.readlines()]
        for i in range(0, len(functions)):
            if len(re.findall('\(', functions[i])) == 1 and len(re.findall('\)', functions[i])) == 0:
                functions[i] = functions[i].replace('(', '\(')
            elif len(re.findall('\(', functions[i])) == 0 and len(re.findall('\)', functions[i])) == 1:
                functions[i] = functions[i].replace(')', '\)')
            if functions[i].endswith('*'):
                functions[i] = functions[i].replace('*', '\\w*')
                functions[i] = '\\b' + functions[i]
            elif functions[i].startswith('*'):
                functions[i] = functions[i].replace('*', '\\w*')
                functions[i] = '\\b' + functions[i]
            else:
                functions[i] = '\\b' + functions[i] + '\\b'

    return functions

def FV_header():
    try:
        year = ['Year']

        tmp_MB_teman_header = [header for header in sorted(os.listdir(prop.MB_teman_filepath)) if header != ".DS_Store"]

        MB_teman_header = [x.replace(".txt","") for x in tmp_MB_teman_header]

        header_feature = year + MB_teman_header

        features = year + MB_teman_header

    except Exception:
        traceback.print_exc()

    return header_feature, year, features

def filter_text_with_verb(text):
    table = str.maketrans({key: None for key in string.punctuation})
    text = text.translate(table)
    text = remove_verb(text)

    return text


def remove_punctuation(text):
    table = str.maketrans({key: None for key in string.punctuation})
    text = text.translate(table)
    text = cleanText(text)
    return text

def remove_verb(text):
    verb_list = [word.strip() for word in read_text_file(prop.verb_filepath)]
    text = [word for word in nltk.word_tokenize(text) if word not in verb_list]

    return text

def filter_text(text):
    table = str.maketrans({key: None for key in string.punctuation})
    text = text.translate(table)

    return text

def word_counter(year, text, article_name):
    # text = "Det Muslimska islamister tog ytterligare Mohammad Mursi 28 platser i Egyptens muslimer på lördagen, sade islamistgruppen på söndagen."
    text = filter_text(text)

    try:
        features, tmp_year, header_feature = FV_header()

        tmp_filepath = os.path.join(prop.feature_vector_filepath, article_name + ".tsv")

        if not os.path.exists(tmp_filepath):
            create_file_with_header(tmp_filepath, header_feature)

        col = 0
        row = 0

        vector = np.zeros((1, len(features))).astype(object)
        vector[:,0] = vector[:,0].astype(int)

        x = text.lower()
        split_text = x.split()
        text_size = len(split_text)

        for feat in features:
            if col < len(tmp_year):
                vector[row][col] = year

            elif col < len(tmp_year) + len(features):
                MB_teman_filepath = os.path.join(prop.MB_teman_filepath, feat + ".txt")
                MB_teman_words = return_words_frequency(MB_teman_filepath)

                count = 0
                try:
                    for single_word in MB_teman_words:
                        count += sum(1 for i in re.finditer(single_word, x))
                        # print(feat, single_word, count)
                    avg_count = round(count / text_size, 5)

                    vector[row][col] = avg_count
                except Exception as e:
                    print(e)

            if col == len(features) - 1:
                col = 0
                break
            col += 1

        with open(tmp_filepath, 'ab') as f_handle:
            np.savetxt(f_handle, vector, delimiter="\t", fmt="%s")


    except Exception:
        traceback.print_exc()

