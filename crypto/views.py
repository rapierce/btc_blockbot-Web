from django.shortcuts import render
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import requests
import static

# Create your views here.
def home(request):
    #Get Top Crypto Data from CoinGecko
    cg_Url = 'https://api.coingecko.com/api/v3/coins/markets'
    cg_Parameters = {'vs_currency':'USD', 'limit':'100', 'sparkline':False}
    
    session = Session()

    try:
        cg_Response_Request = session.get(cg_Url, params=cg_Parameters)
        cg_Data = json.loads(cg_Response_Request.content)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    # #Get Crypto News
    crypto_News_Request = requests.get('https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
    crypto_News = json.loads(crypto_News_Request.content)

    return render(request, 'crypto/home.html', {'crypto_News':crypto_News, 'cg_Data':cg_Data})

def all_marketcap(request):
    #Get Top Crypto Data from CoinGecko
    cg_Marketcap_Url = 'https://api.coingecko.com/api/v3/coins/markets'
    cg_Marketcap_Parameters = {'vs_currency':'USD', 'limit':'100', 'sparkline':False}
    
    session = Session()

    try:
        cg_Marketcap_Request = session.get(cg_Marketcap_Url, params=cg_Marketcap_Parameters)
        cg_Marketcap_Data = json.loads(cg_Marketcap_Request.content)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return render(request, 'crypto/all_marketcap.html', {'cg_Marketcap_Data':cg_Marketcap_Data})

def crypto_Prices(request):
    
    if request.method == 'POST':

        coinLookup = request.POST['coinLookup']
        coinLookup = coinLookup.lower()

        coinLookup = convert_Id(coinLookup)
        print(coinLookup)
        cg_Coin_Url = 'https://api.coingecko.com/api/v3/coins/'
        # cg_Coin_Parameters = {'id':coinLookup}
    
        session2 = Session()
        #session2.headers.update()

        try:
            cg_Coin_Response_Request = session2.get(cg_Coin_Url + coinLookup)
            cg_Coin_Data = json.loads(cg_Coin_Response_Request.content)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        print(cg_Coin_Data['description']['en'])
        return render(request, 'crypto/crypto_Prices.html', {'coinLookup':coinLookup, 'cg_Coin_Data':cg_Coin_Data})
    else:
        not_Found = "Enter a crypto symbol in the [Lookup Crypto] box"
        return render(request, 'crypto/crypto_Prices.html', {'not_Found':not_Found})

def convert_Id(coinLookup):
    session = Session()

    cg_Coin_List_Url = 'https://api.coingecko.com/api/v3/coins/list'
    cg_Coin_List_Request = session.get(cg_Coin_List_Url)
    cg_Coin_List = json.loads(cg_Coin_List_Request.content)

    for coin_List in cg_Coin_List:
            if coinLookup == coin_List['symbol']:
                coinLookup = coin_List['id']
                print(coinLookup)
    return(coinLookup)
