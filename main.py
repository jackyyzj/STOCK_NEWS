import requests
from twilio.rest import Client
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")

Frictional_Number = os.environ.get("Frictional_Number")
My_Number = os.environ.get("My_Number")


stock_params = {
	"function": "TIME_SERIES_DAILY_ADJUSTED",
	"symbol": STOCK_NAME,
	"apikey": STOCK_API_KEY,
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_params)

data = response.json()["Time Series (Daily)"]
data_list = [price for (date, price) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]


day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]


difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
print(difference)

diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)
up_down = None

if diff_percent > 0:
	up_down = "🔺"
else:
	up_down = "🔻"


if abs(diff_percent) > 3:
	news_params = {
		"apiKey": NEWS_API_KEY,
		"qInTitle": COMPANY_NAME,
	}
	news_response = requests.get(NEWS_ENDPOINT, params=news_params)
	articles = news_response.json()["articles"]
	three_articles = articles[:1]
	formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
	print(formatted_articles)

	client = Client(account_sid, auth_token)

	for article in formatted_articles:

		message = client.messages.create(
			body= article[:10],
			from_= Frictional_Number,
			to= My_Number
		)
