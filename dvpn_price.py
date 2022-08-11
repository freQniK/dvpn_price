# ONLY FOR dVPN Nodes v0.3.2
# sudo apt install python3-pip
# sudo pip install toml pycoingecko
# sudo python3 dvpn_coin_conf.py

import toml
from pycoingecko import CoinGeckoAPI 
from os import path
import argparse
import datetime
import time
from statistics import mean


# If not specified, node provider will charge this rate.
# $0.005/GB
PRICE = 5.00
GB    = 1000

# if not specified with --user username this is the default. i.e.,
# /home/sentinel/.sentinelnode/config.toml
USERBASEDIR = "/home/sentinel"

IBCSCRT  = 'ibc/31FEE1A2A9F9C01113F90BD0BBCCE8FD6BBB8585FAF109A2101827DD1D5B95B8'
IBCATOM  = 'ibc/A8C2D23A1E6F95DA4E48BA349667E322BD7A6C996D8A4AAE8BA72E190F3D1477'
IBCDEC   = 'ibc/B1C0DDB14F25279A2026BC8794E12B259F8BDA546A3C5132CCAEE4431CE36783'
IBCOSMO  = 'ibc/ED07A3391A112B175915CD8FAF43A2DA8E4790EDE12566649D0C2F97716B8518'

COINS = {'sentinel' : 'dvpn', 'osmosis' : IBCOSMO, 'decentr' : IBCDEC, 'cosmos' : IBCATOM, 'secret' : IBCSCRT}

SATOSHI = 1000000

def CoinGeckoPrices(days):
    cg = CoinGeckoAPI()
    today = datetime.datetime.now()
    #CoinPrices = cg.get_price(list(COINS.keys()), 'usd')
    CoinPrices = {}
    price_data = {coin: [] for coin in list(COINS.keys())}
    for k in range(1,days+1):
        for coin in list(COINS.keys()):    
            delta = datetime.timedelta(days=k)
            yesterday = today - delta
            data = cg.get_coin_history_by_id(id=coin, date=yesterday.strftime("%d-%m-%Y"),vs_currencies='usd')
            price_data[coin].append(data["market_data"]["current_price"]["usd"])
            #print(price_data[coin])
            time.sleep(10)
            
    for coin in list(COINS.keys()):
        CoinPrices[coin] = mean(price_data[coin])
    #print(CoinPrices)
    return CoinPrices

def CalculateRate(coin_price):
    return (float(PRICE/float((GB*coin_price))))*SATOSHI

if __name__ == "__main__":
    IBCPRICES = {}
    parser = argparse.ArgumentParser(description="dVPN Price Oracle for dVPN Node operators v0.3.2")
    parser.add_argument('-t', '--twap', help="Time Weighted Average Price. --twap days", metavar='twap')
    parser.add_argument('-p', '--price', help="Set the price per GB you would like to charge in USD. i.e., --price 0.005", metavar='price')
    parser.add_argument('-u', '--user', help="Set the base directory where .sentinelnode/ exists i.e., --user dvpn - implies (/home/dvpn/.sentinelnode)", metavar='user')
    args = parser.parse_args()
    
    

    if args.twap:
        days = int(args.twap)
    else:
        days = 1
    CoinPrices = CoinGeckoPrices(days)
    
    if args.price:
        PRICE = GB*float(args.price)

    if args.user:
        USERBASEDIR = '/home/' + args.user
    
    BASEDIR  = path.join(USERBASEDIR, '.sentinelnode')
    
    for coin in CoinPrices.keys():
        if 'sentinel' in coin:
            IBCPRICES['udvpn'] = int(CalculateRate(CoinPrices[coin]))
        else:
            IBCPRICES[COINS[coin]] = int(CalculateRate(CoinPrices[coin]))
            
    print(IBCPRICES)
    
    
    with open(path.join(BASEDIR,'config.toml')) as CONF:
        toml_string = CONF.read()
    DVPNCONFIG = toml.loads(toml_string)
    print(DVPNCONFIG['node']['price'])
    NodePrices = []
    for k,v in IBCPRICES.items():
        NodePrices.append(''.join([str(v),str(k)]))
    
    node_price_string = ''
    for np in NodePrices:
        node_price_string = ','.join([node_price_string, np])
    node_price_string = node_price_string.replace(',','',1)
    print(node_price_string)
    DVPNCONFIG['node']['price'] = node_price_string
    CONF = open(path.join(BASEDIR,'config.toml'), 'w')
    toml.dump(DVPNCONFIG, CONF)
    
