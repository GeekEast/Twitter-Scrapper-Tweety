import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from DataClean import Cleaner


def lag(data, n=1):
    data = list(data)
    lagged_data = [data[i] for i in range(n, len(data))]
    for i in range(0, n):
        lagged_data.append(np.nan)
    return pd.Series(lagged_data)


def forcast(file):
    df = pd.read_csv(file)
    df['month'] = df['date'].map(lambda x: x[5:7])
    df['year'] = df['date'].map(lambda x: x[0:4])
    df['day'] = df['date'].map(lambda x: x[8:11])
    df = df[['year', 'month', 'day', 'score', 'magnitude', 'sentiment', 'googleview', 'price', 'volume']]
    gdf = pd.DataFrame(df.groupby(['year', 'month'])[
                           'score', 'magnitude', 'sentiment', 'googleview', 'price', 'volume'].mean()).reset_index()
    gdf['sentiment_lag1'] = lag(gdf['sentiment'])
    gdf['score_lag1'] = lag(gdf['score'])
    gdf['magnitude_lag1'] = lag(gdf['magnitude'])
    gdf['googleview_lag1'] = lag(gdf['googleview'])
    gdf['volume_lag1'] = lag(gdf['volume'])
    gdf['sentiment_lag2'] = lag(gdf['sentiment'], 2)
    gdf['score_lag2'] = lag(gdf['score'], 2)
    gdf['magnitude_lag2'] = lag(gdf['magnitude'], 2)
    gdf['googleview_lag2'] = lag(gdf['googleview'], 2)
    gdf['volume_lag2'] = lag(gdf['volume'], 2)
    gdf['sentiment_lag3'] = lag(gdf['sentiment'], 3)
    gdf['score_lag3'] = lag(gdf['score'], 3)
    gdf['magnitude_lag3'] = lag(gdf['magnitude'], 3)
    gdf['googleview_lag3'] = lag(gdf['googleview'], 3)
    gdf['volume_lag3'] = lag(gdf['volume'], 3)
    gdf['price_lag1'] = lag(gdf['price'])
    gdf['price_lag2'] = lag(gdf['price'], 2)
    gdf['price_lag3'] = lag(gdf['price'], 3)
    gdf = gdf.dropna()
    reg = LinearRegression().fit(gdf[['sentiment', 'score', 'magnitude', 'googleview', 'volume', 'price_lag1']],
                                 gdf[['price_lag2']])
    print("Variable Regression R Square")
    score = reg.score(gdf[['sentiment', 'score', 'magnitude', 'googleview', 'volume', 'price_lag1']],
                      gdf[['price_lag2']])
    print(score)
    prediction = reg.predict(gdf[['sentiment', 'score', 'magnitude', 'googleview', 'volume', 'price_lag1']].iloc[
                             gdf.shape[0] - 1:gdf.shape[0]])
    prediction = (round(prediction[0][0] * 0.9, 2), round(prediction[0][0] * 1.1, 2))
    print('The interval of the next month prediction:')
    print(prediction)


if __name__ == '__main__':
    cleaner = Cleaner('price_raw.csv',
                      'volume_raw.npy',
                      'bitcoin_raw.csv',
                      'sentiment_raw.csv', )
    final_file = cleaner.clean()
    forcast(final_file)
