import yfinance as yf
from json import JSONDecodeError

# giving the start and end dates
startDate = '2015-03-01'
endDate = '2017-03-01'

# setting the ticker value
ticker = 'GOOGL'

# downloading the data of the ticker value between
# the start and end dates
resultData = yf.download(ticker, startDate, endDate)

# printing the last 5 rows of the data
print(resultData.tail())
