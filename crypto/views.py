

from django.shortcuts import render
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import simplejson as json
import requests
import static
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from datetime import datetime

# Create your views here.
def home(request):
    #Get Top Crypto Data from CoinGecko
    cg_Url = 'https://api.coingecko.com/api/v3/coins/markets'
    cg_Parameters = {'vs_currency':'USD', 'price_change_percentage':'1h,24h,7d,1y', 'sparkline':False}
    
    session = Session()

    try:
        cg_Response_Request = session.get(cg_Url, params=cg_Parameters)
        cg_Data = json.loads(cg_Response_Request.content)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    block_Ex = block_list(True)
    
    # #Get Crypto News
    crypto_News_Request = requests.get('https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
    crypto_News = json.loads(crypto_News_Request.content)

    return render(request, 'crypto/home.html', {'crypto_News':crypto_News, 'block_Ex':block_Ex, 'cg_Data':cg_Data})

def all_marketcap(request):
    #Get Top Crypto Data from CoinGecko
    cg_Marketcap_Url = 'https://api.coingecko.com/api/v3/coins/markets'
    cg_Marketcap_Parameters = {'vs_currency':'USD', 'price_change_percentage':'1h,24h,7d,1y', 'sparkline':False}
    
    session = Session()

    try:
        cg_Marketcap_Request = session.get(cg_Marketcap_Url, params=cg_Marketcap_Parameters)
        cg_Marketcap_Data = json.loads(cg_Marketcap_Request.content)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return render(request, 'crypto/all_marketcap.html', {'cg_Marketcap_Data':cg_Marketcap_Data})

def all_news(request):

    # #Get Crypto News
    all_Crypto_News_Requests = requests.get('https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
    all_Crypto_News = json.loads(all_Crypto_News_Requests.content)

    return render(request, 'crypto/all_news.html', {'all_Crypto_News':all_Crypto_News})

def crypto_Prices(request):
    
    if request.method == 'POST':

        coinLookup = request.POST['coinLookup']
        coinLookup = coinLookup.lower()

        coinLookup, coin_Found = convert_Id(coinLookup)
    
        cg_Coin_Url = 'https://api.coingecko.com/api/v3/coins/'
        
        session2 = Session()
        
        try:
            cg_Coin_Response_Request = session2.get(cg_Coin_Url + coinLookup)
            cg_Coin_Data = json.loads(cg_Coin_Response_Request.content)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        
        return render(request, 'crypto/crypto_Prices.html', {'coinLookup':coinLookup, 'cg_Coin_Data':cg_Coin_Data, 'coin_Found':coin_Found})
    elif request.method == 'GET':
        coinLookup = request.GET['coinLookup']
        coinLookup = coinLookup.lower()

        coinLookup, coin_Found = convert_Id(coinLookup)

        cg_Coin_Url = 'https://api.coingecko.com/api/v3/coins/'
        
        session2 = Session()
        
        try:
            cg_Coin_Response_Request = session2.get(cg_Coin_Url + coinLookup)
            cg_Coin_Data = json.loads(cg_Coin_Response_Request.content)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
        
        return render(request, 'crypto/crypto_Prices.html', {'coinLookup':coinLookup, 'cg_Coin_Data':cg_Coin_Data, 'coin_Found':coin_Found})
    else:
        not_Found = "Enter a crypto symbol in the [Lookup Crypto] box"
        return render(request, 'crypto/crypto_Prices.html', {'not_Found':not_Found})

def convert_Id(coinLookup):
    session = Session()

    cg_Coin_List_Url = 'https://api.coingecko.com/api/v3/coins/list'
    cg_Coin_List_Request = session.get(cg_Coin_List_Url)
    cg_Coin_List = json.loads(cg_Coin_List_Request.content)

    coin_Found = False

    for coin_List in cg_Coin_List:
        if coinLookup == coin_List['symbol']:
            coinLookup = coin_List['id']
            coin_Found = True
            break
        elif coinLookup == coin_List['id']:
            coin_Found = True
            break

    return(coinLookup, coin_Found)

def block_trans(request):
    #working on it
    return

def block_list(request):
    with open('/home/pierce/environments/block_api_env/block_api/keys/blockapi.txt') as block_Api:
        block_Dic = json.load(block_Api)

    block_Dic['block_Info'].reverse()

    # ts = block_Dic['block_Info']['b_Time'][0]
    # time_Convert = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    if request is True:
        request = False
        return block_Dic
    else:
        return render(request, 'crypto/block_list.html', {'block_Dic':block_Dic})

def block_explorer(request):
    with open(r'static/keys/tokens.txt', 'r') as keys_File:
        keys = [line.rstrip('\n') for line in keys_File]

    # Get BlockBot Login Info
    rpc_user = keys[1]
    rpc_password = keys[2]
    block_Value = 0

    # rpc_user and rpc_password are set in the bitcoin.conf file
    rpc_connection = AuthServiceProxy("http://%s:%s@10.6.69.15:8332"%(rpc_user, rpc_password))

    request.method == 'GET'
    get_Block_Hash = (request.GET['get_Block'])
        
    # Pulling information from the Blockchain
    # get_Block_Hash = rpc_connection.getblockhash(block_Num)
    block_Hash = rpc_connection.getblock(get_Block_Hash)
    block_Num = block_Hash['height']
    transactions = block_Hash['tx']
    trans_Dict = {}
    trans_Dict['key'] = []
    block_Value = 0
    ts = block_Hash['time']
    time_Convert = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    coinbase = 'Coinbase'
    address_Dict = {}
    address_Dict['trx'] = []


    for txid in transactions:
        
        #address_Dict['Transaction'] = []
        temp_Address_Dict = {}
        temp_Address_Dict[txid] = []
        tx_Value = 0
        raw_Tx = rpc_connection.getrawtransaction(txid)
        decoded_Tx = rpc_connection.decoderawtransaction(raw_Tx)
        segwit_Test = raw_Tx[8:10]
        # If segwit transaction it adds the appropriate flag (True) to the transaction
        #   ensuring it will be processed as a segwit transaction
        # Adds the transaction out values to the total block value
        if segwit_Test != '00':
            trans_Dict['key'].append(decoded_Tx)
            for output in decoded_Tx['vout']:
                tx_Value = tx_Value + output['value']
            
                if output['value'] > 0:
                    scriptPubKey_Data = (output['scriptPubKey'])
                    script_Dict = {'scriptPubKey':scriptPubKey_Data}
                    for script_Key, script_Value in script_Dict.items():
                        if script_Value['addresses']:
                            for adds in script_Value['addresses']:
                                #print (adds)
                                temp_Address_Dict.get(txid).append(adds)
            block_Value = block_Value + tx_Value
        else:
            flag = True
            segwit_Tx = rpc_connection.decoderawtransaction(raw_Tx, flag)
            trans_Dict['key'].append(segwit_Tx)
            for output in segwit_Tx['vout']:
                tx_Value = tx_Value + output['value']
            
                if output['value'] > 0:
                    scriptPubKey_Data = (output['scriptPubKey'])
                    script_Dict = {'scriptPubKey':scriptPubKey_Data}
                    for script_Key, script_Value in script_Dict.items():
                        if script_Value['addresses']:
                            for adds in script_Value['addresses']:
                                #print (adds)
                                temp_Address_Dict.get(txid).append(adds)
            block_Value = block_Value + tx_Value

        address_Dict.get('trx').append(temp_Address_Dict)

    print (address_Dict)
        
        
    return render(request, 'crypto/block_explorer.html', {'block_Num':block_Num, 'block_Hash':block_Hash, 'block_Value':block_Value, 'trans_Dict':trans_Dict,  'time_Convert':time_Convert, 'address_Dict':address_Dict, 'coinbase':coinbase})


