#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import pandas as pd
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


def run(topic='bitcoin', record_limit=30):
    result = []
    tweet_nlp_engine = TweetNLPEngine()
    with open(topic + ".csv", 'rb') as f:
        line = f.readline().decode('utf-8')
        limit = 0
        while line and limit < record_limit:
            m = re.search(r'^(\d{4}-\d{2}-\d{2}),(.*)', str(line).strip())
            dic = {}
            if m:
                print('***************************')
                time = m.group(1)
                text = m.group(2)
                print('-- Analysing Record ' + str(limit) + ' --')
                try:
                    sentiment = tweet_nlp_engine.analyse_sentiment(text)
                except:
                    line = f.readline().decode('utf-8')
                    limit += 1
                    print('error happened')
                    print('---------------------------------------')
                    continue
                else:
                    score = round(float(sentiment[0]), 3)
                    print(score)
                    magnitude = sentiment[1]
                    print('-- Analysed Record ' + str(limit) + ' --')
                    dic['time'] = time
                    dic['text'] = text
                    dic['score'] = score
                    dic['magnitude'] = magnitude
                    try:
                        result.append(dic)
                    except:
                        print("Fail to add one record to result.")

            line = f.readline().decode('utf-8')
            limit += 1
        print('***************************')
    return result


if __name__ == "__main__":
    topic = input("Please enter the topic, for example-bitcoin: ")
    limit = int(input("Please enter the numer of record to analyze: "))
    if limit == -1:
        limit = 100000000000
    result = run(topic=topic, record_limit=limit)
    df = pd.DataFrame(result)
    df = df.round({'score': 3, 'magnitude': 3})
    pd.set_option('precision', 3)
    df = df[['time', 'score', 'magnitude', 'text']]
    df.to_csv(topic + "_sentiment.csv", index=False)
    print("Result saved as " + topic + "_sentiment.csv")
    print("Sample Result is: ")
    print(df.head())
