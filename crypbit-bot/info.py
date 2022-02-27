from requests.sessions import Session
import os
import json
from dotenv import load_dotenv
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

def getCoinDesc(tickerName):
    slug = {'btc' : ['1', 'bitcoin'], 'eth':['1027', 'ethereum'], 'doge' : ['74','dogecoin']}
    if tickerName in slug:
        parameters['slug'] = slug[tickerName][1]
        id = slug[tickerName][0]
    try:
        response = session.get(url,params=parameters)
        Data = json.loads(response.text)['data'][id]
        tickerDec =Data['description']
        tickerTitle =Data['name']
        tickerLogo = Data['logo'] 
        tickerDetails =[tickerDec, tickerTitle, tickerLogo]
        return tickerDetails
    except:
        print("Ticker Not Found")






