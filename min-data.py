import requests
from pymongo import MongoClient
# from datetime import datetime
import datetime

ts = 1478874600
utc_dt = datetime.datetime.utcfromtimestamp(ts)
print(utc_dt)

client = MongoClient('localhost', 27017)
db = client.data
min_datas = db.min_data
url = "https://www.google.com/finance/getprices?q=AAPL&i=60&p=1d&f=d,o,h,l,c,v"
symbol = "AAPL"
response = requests.get(url)
tokenString = response.text.split("\n")

index = 0
for token in tokenString[8:]:
    # prevent from processing empty string
    if not token:
        continue

    if index == 0:
        time = utc_dt
    else:
        time_index = token.split(",")[0]
        time = utc_dt + datetime.timedelta(0, int(time_index) * 60)

    price = token.split(",")[1]
    min_data = {"_id": symbol + "-" + time.strftime("%Y-%m-%d-%H-%M"),
                "symbol": symbol,
                "price": price,
                "time": time}
    data_id = min_datas.insert_one(min_data).inserted_id
    index = index + 1
