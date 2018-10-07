import sys
import time
import pymongo
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class Tweet:

    def __init__(self, topic, database='scrapper', mongodb_ip='172.17.0.2', mongodb_port=27017, begin_date='20100430',
                 end_date='20180901', scroll_limit=250, time_limit=30000):
        self.__topic = topic
        self.__begin_date = begin_date
        self.__end_date = end_date
        self.__scroll_limit = scroll_limit
        self.__time_limit = time_limit
        self.__browser = None
        self.__result = []
        self.__chrome_options = Options()
        self.__client = pymongo.MongoClient(mongodb_ip, mongodb_port)
        self.__db = self.__client[database]
        self.__collection = self.__db[topic]

    def __gen_url_list(self):
        x = [datetime.strftime(x, '%Y-%m-%d') for x in
             list(pd.date_range(start=self.__begin_date, end=self.__end_date, freq='d'))]
        y = [(self.__topic, x[i], x[i + 1]) for i in range(0, len(x)) if i + 1 < len(x)]
        return ["https://twitter.com/search?l=&q={0}%20since%3A{1}%20until%3A{2}&src=typd".format(*i) for i in y]

    def __load_page(self, url):
        self.__chrome_options.add_argument('--headless')
        self.__chrome_options.add_argument('--disable-gpu')
        self.__chrome_options.add_argument('--no-sandbox')
        self.__browser = webdriver.Chrome(executable_path='/usr/local/share/chromedriver',
                                          chrome_options=self.__chrome_options)
        self.__browser.get(url)
        time.sleep(1)
        self.__browser.find_element_by_xpath('//*[@id="page-container"]/div[2]/div/div/div[1]/div[1]/div[1]').click()
        time.sleep(1)
        count = 0
        start_time = time.time()
        end_time = time.time()
        last_height = self.__browser.execute_script("return document.body.scrollHeight")
        new_height = last_height + 0.001
        while last_height < new_height and count < self.__scroll_limit and end_time - start_time <= self.__time_limit:
            self.__browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)
            last_height = new_height
            new_height = self.__browser.execute_script("return document.body.scrollHeight")
            count += 1
            end_time = time.time()

    def __scrap_tweet_one_page(self):
        html = self.__browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        collections = soup.find_all(class_='content')
        for i in collections:
            dic = {}
            dic['time'] = i.find(class_='stream-item-header').find(class_='time').find('a')['title']
            dic['content'] = i.find(class_='js-tweet-text-container').find('p').text
            try:
                self.__collection.insert_one(dic)
                print('succeed to mongodb')
            except Exception as e:
                print('fail to mongodb')
        self.__browser.close()

    def pull(self):
        url_list = self.__gen_url_list()
        for i in url_list:
            try:
                self.__load_page(i)
                self.__scrap_tweet_one_page()
            except NoSuchElementException as e:
                continue


if __name__ == "__main__":
    topic = str(sys.argv[1])
    begin_date = str(sys.argv[2])
    tweet = Tweet(topic=topic, begin_date=begin_date)
    tweet.pull()
