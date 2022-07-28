import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?q=bitcoin&apiKey=5e3ae26cd50e4508b02c7b03aa9be2fb"

STOCK_API_KEY=" KOOTWG4CN55EDF27"
NEWS_API_KEY="5e3ae26cd50e4508b02c7b03aa9be2fb"
TWILIO_SID= "AC3b456778f82d5e68dd7ebf1113cb495a"
TWILIO_AUTH_TOKEN="a964e1d5b64009e45e717f28464338a6"


## fetching the daily details about yesterday
## using requests
stock_params = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY,
}

response=requests.get(STOCK_ENDPOINT,params=stock_params)
##print(response.json())
data=response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in data.items()]
# print(data_list)
yesterday_data =data_list[0]
yesterday_closing_price=yesterday_data["4. close"]
print(yesterday_closing_price)
day_before_yesterday_data =data_list[1]
day_before_yesterday_closing_price=day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)


## checking the difference between day before yesterdays final price and yesterdays final price

difference = abs(float(yesterday_closing_price)-float(day_before_yesterday_closing_price))
print(difference)


## taking out the percentage at which the data have changed
diff_prcnt=(difference/float(yesterday_closing_price))*100
print(diff_prcnt)

## a note here that if the data percentage we get is greater than 5% so we will give a news to the user

if diff_prcnt>5:
    news_params={
        "apiKey":NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response=requests.get(NEWS_ENDPOINT,params=news_params)
    article=news_response.json()["articles"]
    print(article)
    ## through this we can see what are the articles we will get

    three_articles=article[:3]
    print(three_articles)
    ## so these are the top three articles from the all articles related to this company


    formatted_article_list=[f"Headline: {article ['title']}. \nBrief:{article ['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_article_list:
        message = client.messages.create(
            body=article,
            from_="+17432007160",
            to="+919528656038",
        )
