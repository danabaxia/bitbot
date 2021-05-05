import requests 
import json
import pandas as pd 

key = '3711ff28a46fd9f7cbc915ca70a67b30'
#get cypto historical prices 
def request_CyptoPrice_hour():
    try:
        r = requests.get('https://financialmodelingprep.com/api/v3/historical-chart/1hour/BTCUSD?apikey=' + key)

        data = r.json()
        print(data)
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
        print(type(r))
        data = r.json()['historical']
        print(type(data))
        _data = {}
        for line in data[:30]:
            _data[line["date"]] = line['close']
            
        return _data
    except Exception as exc:
        print('error: ',exc)

def get_cypto_price():
        try:
            r = requests.get('https://financialmodelingprep.com/api/v3/quote/BTCUSD?apikey=' + key)
            return r.json()[0]['price']
        except Exception as exc:
            print('error: ',exc)
            



if __name__ == '__main__':
    request_CyptoPrice_day()
