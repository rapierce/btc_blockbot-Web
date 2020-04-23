from django.shortcuts import render

# Create your views here.
def home(request):
    import requests
    import json

    #get Crypto Price
    crypto_Price_Request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,ETH,LTC,USDT&tsyms=USD')
    crypto_Price = json.loads(crypto_Price_Request.content)

    #Get Crypto News
    crypto_News_Request = requests.get('https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
    crypto_News = json.loads(crypto_News_Request.content)

    return render(request, 'crypto/home.html', {'crypto_News':crypto_News, 'crypto_Price':crypto_Price})

def crypto_Prices(request):
    import requests
    import json
    if request.method == 'POST':
        quote = request.POST['quote']
        quote = quote.upper()
        crypto_Quote_Request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + quote + '&tsyms=USD')
        crypto_Quote = json.loads(crypto_Quote_Request.content)
        return render(request, 'crypto/crypto_Prices.html', {'quote':quote, 'crypto_Quote':crypto_Quote})
    else:
        not_Found = "Enter a crypto symbol in the [Lookup Crypto] box"
        return render(request, 'crypto/crypto_Prices.html', {'not_Found':not_Found})