from requests.sessions import Session
import os
import json
from dotenv import load_dotenv
from nltk import tokenize
load_dotenv()

coinAPI = os.environ.get('COIN_MAKET_API')

url ='https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'

parameters={
    'slug':'bitcoin',
}
headers ={
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': coinAPI
}

session = Session()
session.headers.update(headers)

#to get crypto details and logo
def getCoinDesc(tickerName):
    slug = {'btc' : ['1', 'bitcoin'], 'eth':['1027', 'ethereum'], 'doge' : ['74','dogecoin'], 'sol':['5426', 'solana'], 'bnb':['1839', 'bnb'], 'ltc':['2', 'litecoin'], 'dot':['6636', 'polkadot'], 'matic':['3890', 'polygon'], 'usdt':['825', 'tether'], 'xlm':['512', 'stellar']}

    if tickerName in slug:
        parameters['slug'] = slug[tickerName][1]
        id = slug[tickerName][0]
    try:
        response = session.get(url,params=parameters)
        Data = json.loads(response.text)['data'][id]
        tickerDec =Data['description']
        sentList = tokenize.sent_tokenize(tickerDec)
        tickerDec = " ".join(sentList[:-1])

        tickerTitle =Data['name']
        tickerLogo = Data['logo']
        tickerLink = Data['urls']['website'][0]
        tickerDetails =[tickerDec, tickerTitle, tickerLogo, tickerLink]
        return tickerDetails
    except:
        print("Ticker Not Found")