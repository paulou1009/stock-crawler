import requests
url = "https://www.google.com/finance/getprices?q=AAPL&i=60&p=1d&f=d,o,h,l,c,v"
yelp_r = requests.get(url)
print(yelp_r.text)