import  requests


# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=AAPL&apikey=OMYDPCNTORW5SU1O'
r = requests.get(url)
data = r.json()

print(data)





