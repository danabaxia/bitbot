import requests 
import pandas as pd 

key = '3711ff28a46fd9f7cbc915ca70a67b30'
#get cypto historical prices 
def request_CyptoPrice_hour():
    try:
        r = requests.get('https://financialmodelingprep.com/api/v3/historical-chart/1hour/BTCUSD?apikey=' + key)
        return r.json()
    except Exception as exc:
        print('error: ',exc)

def request_CyptoPrice_30min():
    try:
        r = requests.get('https://financialmodelingprep.com/api/v3/historical-chart/30min/BTCUSD?apikey=' + key)
        return r.json()
    except Exception as exc:
        print('error: ',exc)

def request_CyptoPrice_day():
    try:
        r = requests.get('https://financialmodelingprep.com/api/v3/historical-price-full/BTCUSD?apikey=' + key)
        return r.json()['historical']
    except Exception as exc:
        print('error: ',exc)

def get_cypto_price():
        try:
            r = requests.get('https://financialmodelingprep.com/api/v3/quote/BTCUSD?apikey=' + key)
            return r.json()[0]['price']
        except Exception as exc:
            print('error: ',exc)
            
import csv 
import dateutil.parser
from flaskr import db
from flaskr.models import BitPrice

def add_data():
    with open('bitcoin_price.csv', 'r') as f:
        next(f)
        reader = csv.reader(f)
        for row in reader:
            new_entry = BitPrice(row[0], row[1], dateutil.parser.parse(row[2]))
            db.session.add(new_entry)
            db.session.commit()  
    print('finished')

if __name__ == '__main__':
    #while True: 
    price = get_cypto_price()
        #add_data()
    print('bit price ', price)
