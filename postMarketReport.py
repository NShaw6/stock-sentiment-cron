import yfinance as yf
import localShared
from json import JSONDecodeError
from datetime import timedelta, datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
import pandas as pd



# giving the start and end dates
today = datetime.today().strftime('%Y-%m-%d')
yesterday = datetime.today() - timedelta(days = 1)

# setting the ticker value
tickers = localShared.getTickers()
# ticker = 'GOOGL'

# downloading the data of the ticker value between
# the start and end dates
# resultData = yf.download(ticker, yesterday, today)
# https://github.com/ranaroussi/yfinance

def getPercentageIncreaseOrDecrease(open, close): 
    if (open > close): # decrease
        return -((open - close) / open) * 100
    elif (open < close): # increase
        return ((close - open) / open) * 100
    else: 
        return 0.0


        


