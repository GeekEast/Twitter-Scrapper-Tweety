import re
import pandas as pd
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


# the sentimental analyser engine
class TweetNLPEngine:

    # construct with a gcp nlp engine
    def __init__(self, topic, record_limit=30):
        self.__nlp_client = language.LanguageServiceClient()
        self.__topic = topic
        self.__record_limit = record_limit
        self.__result = []

    # configure the engine and analyze
    def __analyse_sentiment(self, text):
        document = types.Document(content=text, type=enums.Document.Type.PLAIN_TEXT)
        sentiment = self.__nlp_client.analyze_sentiment(document=document).document_sentiment
        return sentiment.score, sentiment.magnitude

    def analyse(self):
        with open(self.__topic + ".csv", 'rb') as f:
            line = f.readline().decode('utf-8')
            limit = 0
            # set the limit
            while line and limit < self.__record_limit:
                m = re.search(r'^(\d{4}-\d{2}-\d{2}),(.*)', str(line).strip())
                dic = {}
                if m:
                    print('***************************')
                    time = m.group(1)
                    text = m.group(2)
                    print('-- Analysing Record ' + str(limit) + ' --')
                    # analyze the sentiment
                    try:
                        sentiment = self.__analyse_sentiment(text)
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
                        dic['date'] = time
                        dic['text'] = text
                        dic['score'] = score
                        dic['magnitude'] = magnitude
                        # add the result to the list
                        try:
                            self.__result.append(dic)
                        except:
                            print("Fail to add one record to result.")

                line = f.readline().decode('utf-8')
                limit += 1
            print('***************************')
            # if limit = -1, scrap all the data
            if limit == -1:
                limit = 100000000000
            # store the result into a pandas dataframe
            df = pd.DataFrame(self.__result)
            # deal with the float number
            df = df.round({'score': 3, 'magnitude': 3})
            pd.set_option('precision', 3)
            df = df[['date', 'score', 'magnitude', 'text']]
            df.columns = ['date', 'score', 'magnitude', 'text']
            # store the result into a csv file
            df.to_csv(self.__topic + "_sentiment.csv", index=False)
            print("Result saved as " + self.__topic + "_sentiment.csv")
            print("Sample Result is: ")
            # print a sample of the result
            print(df.head())


if __name__ == "__main__":
    # get the key parameters from user input
    topic = input("Please enter one topic: ")
    record_limit = input("Please enter the number of record to display: ")
    # create a analyser object
    tweet_nlp = TweetNLPEngine(topic=topic, record_limit=int(record_limit))
    # analyse the sentiment
    tweet_nlp.analyse()