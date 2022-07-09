# sudo apt install python3-pip
# sudo pip install toml pycoingecko
# sudo python3 dvpn_coin_conf.py
import toml
from pycoingecko import CoinGeckoAPI 
from os import path

# EDIT THESE. $6.28 for 314 GB or $0.02/GB
PRICE = 6.28
GB    = 314

# EDIT THIS FOR THE BASE DIR OF .sentinelnode DIRECTORY
# i.e., /home/sentinel/.sentinelnode
# /home/sentinel is BASEDIR
USERBASEDIR = "/home/sentinel"

IBCSCRT  = 'ibc/31FEE1A2A9F9C01113F90BD0BBCCE8FD6BBB8585FAF109A2101827DD1D5B95B8'
IBCATOM  = 'ibc/A8C2D23A1E6F95DA4E48BA349667E322BD7A6C996D8A4AAE8BA72E190F3D1477'
IBCDEC   = 'ibc/B1C0DDB14F25279A2026BC8794E12B259F8BDA546A3C5132CCAEE4431CE36783'
IBCOSMO  = 'ibc/ED07A3391A112B175915CD8FAF43A2DA8E4790EDE12566649D0C2F97716B8518'

COINS = {'sentinel' : 'dvpn', 'osmosis' : IBCOSMO, 'decentr' : IBCDEC, 'cosmos' : IBCATOM, 'secret' : IBCSCRT}

SATOSHI = 1000000



BASEDIR  = path.join(USERBASEDIR, '.sentinelnode')


def CoinGeckoPrices():
    cg = CoinGeckoAPI()
    
    CoinPrices = cg.get_price(list(COINS.keys()), 'usd')
    print(CoinPrices)
    return CoinPrices

def CalculateRate(coin_price):
    return (float(PRICE/float((GB*coin_price))))*SATOSHI

if __name__ == "__main__":
    IBCPRICES = {}
    CoinPrices = CoinGeckoPrices()
    for coin in CoinPrices.keys():
        if 'sentinel' in coin:
            IBCPRICES['udvpn'] = int(CalculateRate(CoinPrices[coin]['usd']))
        else:
            IBCPRICES[COINS[coin]] = int(CalculateRate(CoinPrices[coin]['usd']))
            
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
    