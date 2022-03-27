from multiprocessing import Value
from requests.sessions import Session
import os
import json
from dotenv import load_dotenv
load_dotenv()

coinAPI = os.environ.get('COIN_MAKET_API')

url ='https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

parameters={
    'slug':'',
}
headers ={
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': coinAPI
}

session = Session()
session.headers.update(headers)
slug = {'btc' : ['1', 'bitcoin'], 'eth':['1027', 'ethereum'], 'doge' : ['74','dogecoin'], 'sol':['5426', 'solana'], 'bnb':['1839', 'bnb'], 'ltc':['2', 'litecoin'], 'dot':['6636', 'polkadot'], 'matic':['3890', 'polygon'], 'usdt':['825', 'tether'], 'xlm':['512', 'stellar']}

def getTicketPrice (ticker):
    if ticker in slug:
        parameters['slug'] = slug[ticker][1]
        return getCAP(slug[ticker][0])
    else:
        print("ticker not found")

def getCAP(number):
    try:
        response = session.get(url,params=parameters)
        Data = json.loads(response.text)['data'][number]
        name = Data['name']
        price = Data['quote']['USD']['price']
        return name, round(price,3)
    except:
        print("Error")