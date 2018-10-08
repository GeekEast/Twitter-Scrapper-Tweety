import os.path
import pandas as pd
from pytrends.request import TrendReq  # install google package and api


def trends(topic):
    s = pd.date_range(start='1/1/2011', end='9/1/2018', freq='MS')  # start time
    e = pd.date_range(start='1/1/2011', end='10/1/2018', freq='M')  # end time
    pytrends = TrendReq(hl='en-US', tz=0)
    kw_list = [topic]  # topic

    df = None

    for i in range(len(s)):
        frame = s[i].strftime('%Y-%m-%d') + " " + e[i].strftime(
            '%Y-%m-%d')  # set start day of the month and end day of this month
        pytrends.build_payload(kw_list, cat=0, timeframe=frame, geo='', gprop='')  # use googleview api to get the data
        interest_over_time_df = pytrends.interest_over_time()
        if df is None:
            df = interest_over_time_df
        else:
            df = df.append(interest_over_time_df)
    print(len(df.index))
    print(frame)
    df.to_csv('bitcoin.csv', sep=',', encoding='utf-8')


def gettrends(topic, start_date, end_date):
    if not os.path.exists("bitcoin.csv"):
        trends(topic)

    df = pd.read_csv('bitcoin.csv', index_col=0)
    #     print(df.tail(1).index[0])

    return df[(df.index > start_date) & (df.index <= end_date)]


if __name__ == "__main__":
    print("input your topic")
    topic = input()
    print("input your start time yyyy-mm-dd")
    stime = input()
    print("input your end time yyyy-mm-dd")
    etime = input()
    gettrends(topic, stime, etime)
