import requests
from pymongo import MongoClient
# from datetime import datetime
import datetime

client = MongoClient('localhost', 27017)
db = client.data
min_datas = db.min_data
url = "https://www.google.com/finance/getprices?q=AAPL&i=60&p=1d&f=d,o,h,l,c,v"
symbol = "AAPL"
response = requests.get(url)
tokenString = response.text.split("\n")

ts_raw = tokenString[7].split(",")[0]
ts = ts_raw[1:]
utc_dt = datetime.datetime.utcfromtimestamp(float(ts))
index = 0

for token in tokenString[7:]:
    # prevent from processing empty string
    if not token:
        continue

    if index == 0:
        time = utc_dt
    else:
        time_index = token.split(",")[0]
        time = utc_dt + datetime.timedelta(0, int(time_index) * 60)

    price = token.split(",")[1]
    id = symbol + "-" + time.strftime("%Y-%m-%d-%H-%M")
    exist = min_datas.find_one({"_id": id})
    if exist is None:
        min_data = {"_id": id,
                    "symbol": symbol,
                    "price": price,
                    "time": time}
        data_id = min_datas.insert_one(min_data).inserted_id
        print("persisted : " + str(min_data))
    index = index + 1
