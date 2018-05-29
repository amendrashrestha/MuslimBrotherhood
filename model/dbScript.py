__author__ = 'amendrashrestha'

from pymongo import MongoClient

import traceback

client = MongoClient('localhost', 27017) #dsg.foi.se

def get_article_count(article_name):
    db = client.news_article

    collection = db[article_name.lower()]
    try:
        article_count = {}
        article_count_query = collection.aggregate([{"$project": {'month': {'$month': "$date"}, 'year': {'$year':  "$date"}}},
        {'$group': {'_id': {'year': "$year", 'month': "$month"}, 'count': {'$sum': 1}}},
        {'$sort':{'_id': 1}}])

        for single_date_info in article_count_query:
            tmp_article_date = single_date_info['_id']
            year = str(tmp_article_date['year'])
            month = str(tmp_article_date['month'])
            if len(month) == 1:
                month = str(0) + month
            article_date = year +"-"+ month

            article_freq = single_date_info['count']
            article_count[article_date] = article_freq
    except Exception:
        traceback.print_exc()

    return article_count

def get_article_year_count(single_article):
    db = client.news_article

    collection = db[single_article.lower()]
    try:
        article_count = {}
        article_count_query = collection.aggregate([{'$group': {'_id': { '$year': "$date" }, 'count':{'$sum':1}}} ,{'$sort':{'_id': 1}}])

        for single_date_info in article_count_query:
            article_date = single_date_info['_id']

            article_freq = single_date_info['count']
            article_count[article_date] = article_freq
    except Exception:
        traceback.print_exc()

    return article_count

def get_article_year(single_article):
    db = client.news_article

    collection = db[single_article.lower()]
    try:
        article_year = []

        article_count_query = collection.aggregate([{'$group': {'_id': { '$year': "$date" }, 'count':{'$sum':1}}} ,{'$sort':{'_id': 1}}])

        for single_date_info in article_count_query:
            article_date = single_date_info['_id']

            article_year.append(article_date)
    except Exception:
        traceback.print_exc()

    return article_year

def get_articles(article_name):
    db = client.news_article
    collection = db[article_name]

    try:
        post_query = collection.find({}, {"text": True})#.limit(5)
        posts_list = []

        for post in post_query:
            # post = post['text']
            yield post['text']
            # posts_list.append(post)
        # return posts_list

    except Exception:
        traceback.print_exc()


def get_article_with_year(article_name, year):
    db = client.news_article
    collection = db[article_name]

    try:
        post_query = collection.aggregate([{'$project': {'text': "$text", 'year': { '$year': "$date" }}},{ '$match' : { 'year': year} }])

        articles = []

        for post in post_query:
            post = post['text']
            articles.append(post)

        return articles

    except Exception:
        traceback.print_exc()



