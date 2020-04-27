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
    session.headers.update()

    try:
        cg_Response_Request = session.get(cg_Url, params=cg_Parameters)
        cg_Data = json.loads(cg_Response_Request.content)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    # #Get Crypto News
    crypto_News_Request = requests.get('https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
    crypto_News = json.loads(crypto_News_Request.content)

    return render(request, 'crypto/home.html', {'crypto_News':crypto_News, 'cg_Data':cg_Data})

def crypto_Prices(request):
    
    if request.method == 'POST':
        # Open keys.txt file to retrieve rpc User and Password

        with open('static/keys/tokens.txt') as tokens_File:
            token = [line.rstrip('\n') for line in tokens_File]

        cmc_API_Token = token[0]


        coinLookup = request.POST['coinLookup']
        coinLookup = coinLookup.upper()
        crypto_Info_Url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
        crypto_Info_Parameters = {'symbol':coinLookup}
        crypto_Info_Headers = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': cmc_API_Token}

        session = Session()
        session.headers.update(crypto_Info_Headers)

        try:
            crypto_Info_Request = session.get(crypto_Info_Url, params=crypto_Info_Parameters)
            crypto_Info = json.loads(crypto_Info_Request.content)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

        # Change symbol to name exp. BTC -> bitcoin
        if (crypto_Info['status']['error_code']) != 400:
            for x, v in crypto_Info['data'].items():
                coin_Ids = v['slug']
                #print(coin_Ids)
        
            cg_Price_Url = 'https://api.coingecko.com/api/v3/coins/markets'
            cg_Price_Parameters = {'vs_currency':'USD', 'ids':coin_Ids, 'limit':'100', 'sparkline':False}
        
            session2 = Session()
            session2.headers.update()

            try:
                cg_Price_Response_Request = session2.get(cg_Price_Url, params=cg_Price_Parameters)
                cg_Price_Data = json.loads(cg_Price_Response_Request.content)
            except (ConnectionError, Timeout, TooManyRedirects) as e:
                print(e)

            return render(request, 'crypto/crypto_Prices.html', {'coinLookup':coinLookup, 'crypto_Info':crypto_Info, 'cg_Price_Data':cg_Price_Data})
        else:
            return render(request, 'crypto/crypto_Prices.html', {'coinLookup':coinLookup, 'crypto_Info':crypto_Info})

    else:
        not_Found = "Enter a crypto symbol in the [Lookup Crypto] box"
        return render(request, 'crypto/crypto_Prices.html', {'not_Found':not_Found})

        


# def crypto_Prices(request):
    
#     if request.method == 'POST':
#         coinLookup = request.POST['coinLookup']
#         coinLookup = coinLookup.upper()
#         crypto_Info_Request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + coinLookup + '&tsyms=USD')
#         crypto_Info = json.loads(crypto_Info_Request.content)
#         return render(request, 'crypto/crypto_Prices.html', {'coinLookup':coinLookup, 'crypto_Info':crypto_Info})
#     else:
#         not_Found = "Enter a crypto symbol in the [Lookup Crypto] box"
#         return render(request, 'crypto/crypto_Prices.html', {'not_Found':not_Found})