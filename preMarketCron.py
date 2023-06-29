from datetime import timedelta, datetime
from urllib.request import urlopen, Request

import localShared
import pandas as pd
from bs4 import BeautifulSoup
from dateutil.utils import today
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
import yfinance as yf



def convert24(str1):
    # Checking if last two elements of time
    # is AM and first two elements are 12
    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]

    # remove the AM
    elif str1[-2:] == "AM":
        return str1[:-2]

    # Checking if last two elements of time
    # is PM and first two elements are 12
    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]

    else:

        # add 12 to hours and remove PM
        return str(int(str1[:2]) + 12) + str1[2:8]


def is_time_before_market_close(str1):
    # Checking if time is before close
    if int(str1[0:2]) < 16:
        if (int(str1[3:5])) < 1:
            return bool(1)
    return bool(0)


def convert_string_to_datetime(str1):
    datetime_object = datetime.strptime(str1, '%b-%d-%y')
    return datetime_object


web_url = 'https://finviz.com/quote.ashx?t='

news_tables = {}
tickers = localShared.getTickers()

for tick in tickers:
    url = web_url + tick
    req = Request(url=url, headers={"User-Agent": "Chrome"})
    response = urlopen(req)
    html = BeautifulSoup(response, "html.parser")
    news_table = html.find(id='news-table')
    news_tables[tick] = news_table

news_list = []

# for file_name, news_table in news_tables.items():
#     for i in news_table.findAll('tr'):
#         try:
#             getattr(i.a, "get_text")
#             text = i.a.get_text()
#             date_scrape = i.td.text.split()
#             if len(date_scrape) == 1:
#                 time = date_scrape[0]
#             else:
#                 date = date_scrape[0]
#                 time = date_scrape[1]
#                 date_datetime = convert_string_to_datetime(date)
#             tick = file_name.split('_')[0]
#             # twenty_four_hour_time = convert24(time).replace('PM', '')
#             news_list.append([tick, date_datetime, time, text])
#         except AttributeError:
#             continue


for ticker in tickers: 
    yahooInfo = yf.Ticker(str(ticker))
    openValue = yahooInfo.info['open']
    closeValue = yahooInfo.info['currentPrice']
    for article in yahooInfo.news:
        date = datetime.fromtimestamp(article['providerPublishTime'])
        date = date.strftime('%Y-%m-%d 00:00:00 %I:%M%p')
        news_list.append([ticker, date[0:10], date[20:28], article['title']])


# Sentiment Analysis of recent Stock News
vader = SentimentIntensityAnalyzer()
columns = ['ticker', 'date', 'time', 'headline']
news_df = pd.DataFrame(news_list, columns=columns)
scores = news_df['headline'].apply(vader.polarity_scores).tolist()
scores_df = pd.DataFrame(scores)
news_df = news_df.join(scores_df, rsuffix='_right')
today_date = today()
news_df = news_df.query("date == @today_date")
news_df['date'] = pd.to_datetime(news_df.date).dt.date
mean_scores = news_df.groupby(['ticker', 'date']).mean()
email_content = mean_scores.compound.to_string()
print(email_content)