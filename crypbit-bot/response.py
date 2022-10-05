from requests.sessions import Session
import os
import json
from dotenv import load_dotenv
import discord
import nltk
from pymongo import MongoClient
load_dotenv()
# nltk.download('punkt')

mongo_connect = os.environ.get('MONGO_CONNECT')
slug = {'btc' : ['1', 'bitcoin'], 'eth':['1027', 'ethereum'], 'doge' : ['74','dogecoin'], 'sol':['5426', 'solana'], 'bnb':['1839', 'bnb'], 'ltc':['2', 'litecoin'], 'dot':['6636', 'polkadot'], 'matic':['3890', 'polygon'], 'usdt':['825', 'tether'], 'xlm':['512', 'stellar']}
coinAPI = os.environ.get('COIN_MARKET_API')

client = MongoClient(mongo_connect)
database = client['crypbit_test']
collection = database['slug']

parameters={
    'slug':'',
}
headers ={
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': coinAPI
}

session = Session()
session.headers.update(headers)

def check_ticker(ticker):
    query_result = collection.find_one({'symbol':ticker})
    parameters['slug'] = query_result['name'].lower()
    id = str(query_result['_id'])
    return id
        

def getTickerPrice(ticker):
    url ='https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    try:
        id = check_ticker(ticker)
        response = session.get(url,params=parameters)
        Data = json.loads(response.text)['data'][id]
        name = Data['name']
        price = Data['quote']['USD']['price']
        return name, round(price,3)
    except:
        print('Ooops! Ticker not found')


def getCoinDesc(tickerName):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/info"
    try:
        id = check_ticker(tickerName)
        response = session.get(url,params=parameters)
        Data = json.loads(response.text)['data'][id]
        tickerDec =Data['description']
        sentList = nltk.tokenize.sent_tokenize(tickerDec)

        tickerDesc = " ".join(sentList[:-1])
        tickerTitle =Data['name']
        tickerLogo = Data['logo']
        tickerLink = Data['urls']['website'][0]
        tickerDetails =[tickerDesc, tickerTitle, tickerLogo, tickerLink]
        return tickerDetails
    except:
        print("Ticker Not Found")
