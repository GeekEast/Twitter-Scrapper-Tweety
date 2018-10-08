from datetime import datetime
import pandas as pd
import numpy as np
import warnings


class Cleaner:
    def __init__(self, price, volume, goolgeview, sentiment, input='./RawData', output='.'):
        warnings.filterwarnings('ignore')
        self.__price = price
        self.__volume = volume
        self.__googleview = goolgeview
        self.__sentiment = sentiment
        self.__input = input
        self.__output = output

    # clean the price raw data
    def __clean_price(self, file, output=''):
        price = pd.read_csv(file)
        price1 = price[::-1]  # revert the price
        price1['date'] = pd.to_datetime(price1['time'])  # convert string to datetime
        del price1['time']  # remove the time column
        price1.index = price1['date']  # set time as index
        price2 = price1.loc[datetime(2013, 1, 1):datetime(2018, 8, 28)]  # select the required  data
        filename = 'price.csv'
        price2.to_csv(str(output) + "/" + str(filename), index=False)  # save as csv
        return str(output) + "/" + str(filename)

    # clean the google view raw data
    def __clean_trend(self, file, output=''):
        hot_final = pd.read_csv(file)
        hot_final['date'] = pd.to_datetime(hot_final['date'])  # convert string to datetime
        hot_final.index = hot_final['date']  # set time as index
        del hot_final['date']  # remove the time column
        hot_final = hot_final.loc[datetime(2013, 1, 1):datetime(2018, 8, 28)]  # select the required  data
        filename = 'googleview.csv'
        hot_final.columns = ['googleview']
        hot_final.to_csv(str(output) + '/' + str(filename))  # save as csv
        return str(output) + '/' + str(filename)

    # clean the bitcoin volume raw data
    def __clean_volume(self, file, output=''):
        pd.options.display.float_format = '{:20,.2f}'.format
        # Load npy
        results = np.load(file).item()
        df = pd.DataFrame(list(results.items()), columns=['date', 'volume'], dtype=float)  # create the dateframe
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            df['date'] = pd.to_datetime(df['date'])  # convert string to datetime
            df.index = df['date']  # set time as index
            del df['date']  # remove the time column
            df_final = df.loc[datetime(2013, 1, 1):datetime(2018, 8, 28)]  # select the required  data
            filename = 'volume.csv'
            df_final.to_csv(str(output) + '/' + str(filename))  # save as csv
        return str(output) + '/' + str(filename)

    # clean the sentiment raw data
    def __clean_sentiment(self, file, output=''):
        def set_as_nan(x):
            if x == 'time':
                return np.nan
            else:
                return x

        df = pd.read_csv(file)
        df.dropna(how='any', inplace=True)
        df['date'] = df['date'].map(set_as_nan)
        df.dropna(how='any', inplace=True)
        df = df[['date', 'score', 'magnitude']]
        df['score'] = df['score'].map(lambda x: float(x))
        df['magnitude'] = df['magnitude'].map(lambda x: float(x))
        df['sentiment'] = df['score'] * df['magnitude']
        df = pd.DataFrame(df.groupby(['date'])['score', 'magnitude', 'sentiment'].mean())
        df = df.reset_index()
        df = df.sort_values('date')
        df.colums = ['date', 'score', 'magnitude', 'sentiment']
        filename = 'sentiment.csv'
        df.to_csv(str(output) + '/' + str(filename), index=False)
        return str(output) + '/' + str(filename)

    # the clean pipeline
    def clean(self):
        price_path = self.__clean_price(str(self.__input) + "/" + str(self.__price), './CleanData')
        volume_path = self.__clean_volume(str(self.__input) + "/" + str(self.__volume), './CleanData')
        trend_path = self.__clean_trend(str(self.__input) + "/" + str(self.__googleview), './CleanData')
        sentiment_path = self.__clean_sentiment(str(self.__input) + "/" + str(self.__sentiment), './CleanData')
        df = pd.read_csv(sentiment_path)
        df1 = pd.read_csv(trend_path)
        df2 = pd.read_csv(price_path)
        df3 = pd.read_csv(volume_path)

        df1 = df1.sort_values(by='date')
        df1.columns = ['date', 'googleview']
        df1 = df1.reset_index()
        df1 = df1[['date', 'googleview']]

        df2 = df2.sort_values(by='date')
        df2 = df2.reset_index()
        df2 = df2[['date', 'price']]

        df3 = df3.sort_values(by='date')
        df3.columns = ['date', 'volume']
        df3 = df3.reset_index()
        df3 = df3[['date', 'volume']]

        df = df.merge(df1, how='inner', on='date')
        df = df.merge(df2, how='inner', on='date')
        df = df.merge(df3, how='inner', on='date')
        filename = 'final.csv'
        df.to_csv(str(self.__output) + '/' + str(filename), index=False)
        return str(self.__output) + '/' + str(filename)


if __name__ == "__main__":
    cleaner = Cleaner('price_raw.csv',
                      'volume_raw.npy',
                      'bitcoin_raw.csv',
                      'sentiment_raw.csv',
                      )
    print(cleaner.clean())
