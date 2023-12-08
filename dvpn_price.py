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
import requests

VERSION = "v0.4.2"

# If not specified, node provider will charge this rate.
# $0.008/GB,$0.005/hr
GBPRICE = 8.00
HRPRICE = 5.00
GB      = 1000
HR      = 1000

# if not specified with --user username this is the default. i.e.,
# /home/sentinel/.sentinelnode/config.toml
USERBASEDIR = "/home/sentinel"

IBCSCRT  = 'ibc/31FEE1A2A9F9C01113F90BD0BBCCE8FD6BBB8585FAF109A2101827DD1D5B95B8'
IBCATOM  = 'ibc/A8C2D23A1E6F95DA4E48BA349667E322BD7A6C996D8A4AAE8BA72E190F3D1477'
IBCDEC   = 'ibc/B1C0DDB14F25279A2026BC8794E12B259F8BDA546A3C5132CCAEE4431CE36783'
IBCOSMO  = 'ibc/ED07A3391A112B175915CD8FAF43A2DA8E4790EDE12566649D0C2F97716B8518'

COINS = {'sentinel' : 'udvpn', 'osmosis' : IBCOSMO, 'decentr' : IBCDEC, 'cosmos' : IBCATOM, 'secret' : IBCSCRT}

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
            try:
                data = cg.get_coin_history_by_id(id=coin, date=yesterday.strftime("%d-%m-%Y"),vs_currencies='usd')
            except ValueError:
                time.sleep(30)
                try: 
                    data = cg.get_coin_history_by_id(id=coin, date=yesterday.strftime("%d-%m-%Y"),vs_currencies='usd')
                except ValueError:
                    continue
            price_data[coin].append(data["market_data"]["current_price"]["usd"])
            #print(price_data[coin])
            time.sleep(10)
            
    for coin in list(COINS.keys()):
        CoinPrices[coin] = mean(price_data[coin])
    #print(CoinPrices)
    return CoinPrices

def CalculateGBRate(coin_price,coin,minp):
    price = (float(GBPRICE/float((GB*coin_price))))*SATOSHI
    
    for key,value in COINS.items():
        if key == coin:
            for ibc,mu_price in minp.items():
                if value == ibc:
                    if price < float(mu_price):
                        price = float(mu_price)

    return price

def CalculateHrRate(coin_price,coin,minp):
    price = (float(HRPRICE/float((HR*coin_price))))*SATOSHI

    for key,value in COINS.items():
        if key == coin:
            for ibc,mu_price in minp.items():
                if value == ibc:
                    if price < float(mu_price):
                        price = float(mu_price)
    return price

def ParseNodePrices(gb,hr):
    NodeGBPrices = []
    NodeHrPrices = []
    for k,v in gb.items():
        NodeGBPrices.append(''.join([str(v),str(k)]))
    
    node_price_string = ''
    for np in NodeGBPrices:
        node_price_string = ','.join([node_price_string, np])
    node_gb_price_string = node_price_string.replace(',','',1)

    for k,v in hr.items():
        NodeHrPrices.append(''.join([str(v),str(k)]))
    
    node_price_string = ''
    for np in NodeHrPrices:
        node_price_string = ','.join([node_price_string, np])
    node_hr_price_string = node_price_string.replace(',','',1)

    return node_gb_price_string,node_hr_price_string

if __name__ == "__main__":
    print(f"dVPN Price Oracle for dVPN Node operators {VERSION} - freQniK\n\n")
    IBCGBPRICES = {}
    IBCHRPRICES = {}
    parser = argparse.ArgumentParser(description=f"dVPN Price Oracle for dVPN Node operators {VERSION} - freQniK")
    parser.add_argument('-t', '--twap', help="Time Weighted Average Price.", metavar='days')
    parser.add_argument('-p', '--price-gb', help="Set the price per GB you would like to charge in USD. i.e., --price 0.005", metavar='price')
    parser.add_argument('-q', '--price-hr', help="Set the price per hour you would like to charge in USD. i.e., --price 0.005", metavar='hprice')
    parser.add_argument('-u', '--user', help="Set the base directory where .sentinelnode/ exists i.e., --user dvpn - implies (/home/dvpn/.sentinelnode)", metavar='user')
    args = parser.parse_args()
    
    r = requests.get('https://aimokoivunen.mathnodes.com:5000/api/minprices')
    MINPRICES = r.json()
    MIN_GB_PRICES = MINPRICES['MinGB']
    MIN_HR_PRICES = MINPRICES['MinHr']
    print("MIN PRICES: ")
    print(MIN_GB_PRICES)
    print(MIN_HR_PRICES)
    #a = input("Press Enter to continue....")
    

    if args.twap:
        days = int(args.twap)
    else:
        days = 1
    
    
    if args.price_gb:
        GBPRICE = GB*float(args.price_gb)
   
    if args.price_hr:
        HRPRICE = HR*float(args.price_hr)
        
    if args.user:
        USERBASEDIR = '/home/' + args.user
    
    BASEDIR  = path.join(USERBASEDIR, '.sentinelnode')
    print("Getting TWAP prices for all coins from Coingecko....")
    CoinPrices = CoinGeckoPrices(days)
    
    for coin in CoinPrices.keys():
        if 'sentinel' in coin:
            IBCGBPRICES['udvpn'] = int(CalculateGBRate(CoinPrices[coin],coin,MIN_GB_PRICES))
        else:
            IBCGBPRICES[COINS[coin]] = int(CalculateGBRate(CoinPrices[coin],coin,MIN_GB_PRICES))
    
    for coin in CoinPrices.keys():
        if 'sentinel' in coin:
            IBCHRPRICES['udvpn'] = int(CalculateHrRate(CoinPrices[coin],coin,MIN_HR_PRICES))
        else:
            IBCHRPRICES[COINS[coin]] = int(CalculateHrRate(CoinPrices[coin],coin,MIN_HR_PRICES))
    
    
    
    print("GB Prices:")        
    print(IBCGBPRICES)
    print("\n")
    print("Hourly Prices:")
    print(IBCHRPRICES)
    
    
    with open(path.join(BASEDIR,'config.toml')) as CONF:
        toml_string = CONF.read()
    DVPNCONFIG = toml.loads(toml_string)
    #print(DVPNCONFIG['node']['gigabit_prices'])
    #print(DVPNCONFIG['node']['hourly_prices'])
    
    
    node_gb_price_string,node_hr_price_string = ParseNodePrices(IBCGBPRICES, IBCHRPRICES)
    
    print(node_gb_price_string)
    print(node_hr_price_string)
    DVPNCONFIG['node']['gigabyte_prices'] = node_gb_price_string
    DVPNCONFIG['node']['hourly_prices']   = node_hr_price_string
    CONF = open(path.join(BASEDIR,'config.toml'), 'w')
    toml.dump(DVPNCONFIG, CONF)
    