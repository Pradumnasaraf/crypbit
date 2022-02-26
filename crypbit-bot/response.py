from multiprocessing import Value
from requests.sessions import Session
import os
import json
from dotenv import load_dotenv
load_dotenv()
number =''


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

def getTicketPrice (ticker):
    return evaluteTicker(ticker)
        

def evaluteTicker(getSlugName):

    if getSlugName == "btc":
        parameters['slug'] = "bitcoin"
        getCAP('1')
    elif getSlugName == "eth":
        parameters['slug'] = "ethereum"
    elif getSlugName == "doge":
        parameters['slug'] = "dogecoin"
    else:
        print("ticker not found")

def getCAP(number):
    try:
        response = session.get(url,params=parameters)
        Data = json.loads(response.text)['data'][number]['quote']['USD']['price']
        print(Data)
        return Data
    except:
        print("Error")

