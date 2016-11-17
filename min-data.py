import requests
import MySQLdb
import datetime

db = MySQLdb.connect(
    host = "localhost",
    user="root",
    passwd="password",
    db="stock"
)
cur = db.cursor()

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
    exist = cur.execute("SELECT * FROM stock WHERE id = %s", (id,))
    if exist == 0:
        # min_data = {"_id": id,
        #             "symbol": symbol,
        #             "price": price,
        #             "time": time}
        # print("persisted : " + str(min_data))
        cur.execute("INSERT INTO stock(id, symbol, price, date) VALUES (%s, %s, %s, %s)", (id, symbol, price, time.strftime('%Y-%m-%d %H:%M:%S')),)
        db.commit()
    index = index + 1
db.close()