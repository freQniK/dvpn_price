# dvpn_price
Update Sentinel DVPN Node Prices with Market Changes including IBC coin prices based on TWAP (Time Weighted Average Price). Updates the `config.toml` for hourly and gigabyte prices based on this average and user specified price. 

## Note 

This is for dVPN node versions 0.7.0

# Install (binary)

Download the latest version of [dvpn_price](https://github.com/freQniK/dvpn_price/releases/download/v0.4.0/dvpn_price) from the releases page.

# Install (source)
```shell
sudo apt install python3-pip
sudo pip install toml pycoingecko
```

Then run from source:

```shell
sudo ./dvpn_price.py -h
```

# Run

```shell
$ sudo python3 dvpn_price -h
dVPN Price Oracle for dVPN Node operators v0.4.0 - freQniK


usage: dvpn_price.py [-h] [-t days] [-p price] [-q hprice] [-u user]

dVPN Price Oracle for dVPN Node operators v0.4.0 - freQniK

optional arguments:
  -h, --help            show this help message and exit
  -t days, --twap days  Time Weighted Average Price.
  -p price, --price-gb price
                        Set the price per GB you would like to charge in USD.
                        i.e., --price 0.005
  -q hprice, --price-hr hprice
                        Set the price per hour you would like to charge in
                        USD. i.e., --price 0.005
  -u user, --user user  Set the base directory where .sentinelnode/ exists
                        i.e., --user dvpn - implies (/home/dvpn/.sentinelnode)

```

Where **days** in `--twap` is the number of days to average a price over based on market price of the coin for each previous day. 

i.e., 
`-p/--price-gb 0.008` - $0.008/GB
`-q/--price-hr 0.004` - $0.004/hr
`-t/--twap 7` - Average all IBC and DVPN prices over 7 days 

## Example
```shell
sudo dvpn_price --twap 7 --price-gb 0.008 --price-hr 0.005 --user sentinel
```

This will average the price of *OSMO, SCRT, ATOM, DEC, DVPN* over the last 7 days. It will set a price of *$0.008/GB* and *$0.005/hr* and change the **config.toml** in the directory `/home/sentinel/.sentinelnode/config.toml`

### Note
Be sure to run this as `sudo` as the config directory is root permissions only. 

## Cronjob
You can also create a cronjob (as root) to have this run every week, every month, every day, every hour, every minute. Just be sure to restart your node eventually for the changes to take place.

### Example
```shell
sudo crontab -e
```

Place the following line at the bottom of the file:
```
59 12 * * * /home/sentinel/Scripts/dvpn_price --twap 7 --price-gb 0.008 --price-hr 0.005 --user sentinel
```

This will update your sentinel node **config.toml** every day at 12:59 p.m.

