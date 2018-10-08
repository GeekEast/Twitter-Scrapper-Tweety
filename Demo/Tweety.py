from Scrapper import *
from TweetNLPEngine import *

if __name__ == "__main__":
    # get the key parameters from user input
    topic = input("Please enter the topic, for example bitcoin: ")
    begin_date = input("Please enter the begin date, for example 20130530: ")
    end_date = input("Please enter the end date, for example 20130602: ")
    scroll_limit = input("Please enter the time of flipping, for example 50: ")
    time_limit = input("Please enter the expected running time(seconds), for example 300: ")
    record_limit = input("Please enter the limit of records to display: ")
    tweet = Tweet(topic=topic,
                  begin_date=begin_date,
                  end_date=end_date,
                  scroll_limit=int(scroll_limit),
                  time_limit=int(time_limit))
    nlp_engine = TweetNLPEngine(topic=topic, record_limit=int(record_limit))
    # start scrap
    tweet.pull()
    # analyse the sentiment
    nlp_engine.analyse()
