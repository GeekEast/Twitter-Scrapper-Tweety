#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import sys
import pymongo
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


class TweetNLPEngine:

    def __init__(self):
        self.nlp_client = language.LanguageServiceClient()

    def analyse_sentiment(self, text):
        document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
        sentiment = self.nlp_client.analyze_sentiment(document=document).document_sentiment
        return sentiment.score, sentiment.magnitude


def run(mongodb_ip='172.17.0.2', mongodb_port=27017, db_name='scrapper', collection_name='sentiment',
        data_source='bitcoin.csv'):
    mongo_client = pymongo.MongoClient(mongodb_ip, mongodb_port)
    db = mongo_client[db_name]
    collection = db[collection_name]

    tweet_nlp_engine = TweetNLPEngine()
    with open(data_source, 'rb') as f:
        line = f.readline().decode('utf-8')
        print('***************************')
        limit = 0
        while line:
            m = re.search(r'^(\d{4}-\d{2}-\d{2}),(.*)', str(line).strip())
            dic = {}
            if m:
                print('***************************')
                time = m.group(1)
                text = m.group(2)
                print('--------start NLP ' + str(limit) + ' --------')
                try:
                    sentiment = tweet_nlp_engine.analyse_sentiment(text)
                except:
                    line = f.readline().decode('utf-8')
                    limit += 1
                    print('error happened')
                    print('---------------------------------------')
                    continue
                else:
                    score = sentiment[0]
                    magnitude = sentiment[1]
                    print('--------finish NLP ' + str(limit) + ' --------')
                    dic['time'] = time
                    dic['text'] = text
                    dic['score'] = score
                    dic['magnitude'] = magnitude
                    print('add to mongo db')
                    try:
                        collection.insert_one(dic)
                        print("succeed to mongodb")
                    except Exception:
                        print("fail to mongodb")
                    print('---------------------------------------')
            line = f.readline().decode('utf-8')
            limit += 1

    pass


if __name__ == "__main__":
    mongodb_ip = str(sys.argv[1])
    mongodb_port = int(sys.argv[2])
    db_name = str(sys.argv[3])
    collection_name = str(sys.argv[4])
    data_source = str(sys.argv[5])
    run(mongodb_ip, mongodb_port, db_name, collection_name, data_source)
