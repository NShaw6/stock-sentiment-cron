import yfinance as yf
import localShared
from json import JSONDecodeError
from datetime import timedelta, datetime


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
    if (open > close): 
        return (close - open) / open * 100
    elif (open < close): 
        return (open - close) / open * 100
    else: 
        return 0.0

for ticker in tickers: 
    yahooInfo = yf.Ticker(str(ticker))
    openValue = yahooInfo.info['open']
    closeValue = yahooInfo.info['currentPrice']
    print (ticker + ' ' +  str(openValue)  + ' ' + str(closeValue) + ' ' + str(getPercentageIncreaseOrDecrease(openValue, closeValue)))


