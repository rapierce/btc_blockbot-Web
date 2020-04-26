from django.shortcuts import render
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import requests

# Create your views here.
def home(request):

    #Get Top Crypto Data from CoinMarketCap
    cmc_Url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    cmc_Parameters = {'start':'1', 'limit':'5000', 'convert':'USD'}
    cmc_Headers = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': 'efca78fc-363d-46e6-843b-cfb80fb5857b',}

    session = Session()
    session.headers.update(cmc_Headers)

    try:
        cmc_Response_Request = session.get(cmc_Url, params=cmc_Parameters)
        cmc_Data = json.loads(cmc_Response_Request.content)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    #Get Crypto News
    crypto_News_Request = requests.get('https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
    crypto_News = json.loads(crypto_News_Request.content)

    return render(request, 'crypto/home.html', {'crypto_News':crypto_News, 'cmc_Data':cmc_Data})

def crypto_Prices(request):
    
    if request.method == 'POST':
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_Quote_Url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'
        crypto_Quote_Parameters = {'symbol':quote}
        crypto_Quote_Headers = {'Accepts': 'application/json','X-CMC_PRO_API_KEY': 'efca78fc-363d-46e6-843b-cfb80fb5857b',}

        session = Session()
        session.headers.update(crypto_Quote_Headers)

        try:
            crypto_Quote_Request = session.get(crypto_Quote_Url, params=crypto_Quote_Parameters)
            crypto_Quote = json.loads(crypto_Quote_Request.content)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        return render(request, 'crypto/crypto_Prices.html', {'quote':quote, 'crypto_Quote':crypto_Quote})
    else:
        not_Found = "Enter a crypto symbol in the [Lookup Crypto] box"
        return render(request, 'crypto/crypto_Prices.html', {'not_Found':not_Found})


# def crypto_Prices(request):
    
#     if request.method == 'POST':
#         quote = request.POST['quote']
#         quote = quote.upper()
#         crypto_Quote_Request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + quote + '&tsyms=USD')
#         crypto_Quote = json.loads(crypto_Quote_Request.content)
#         return render(request, 'crypto/crypto_Prices.html', {'quote':quote, 'crypto_Quote':crypto_Quote})
#     else:
#         not_Found = "Enter a crypto symbol in the [Lookup Crypto] box"
#         return render(request, 'crypto/crypto_Prices.html', {'not_Found':not_Found})