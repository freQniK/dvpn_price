# dvpn_price
Update Sentinel DVPN Node Prices with Market Changes

## Note 

This is for dVPN node versions 0.3.2

# Install (binary)

Download the latest version of **dvpn_price** from our the releases page.



# Install (source)
```shell
sudo apt install python3-pip
sudo pip install toml pycoingecko
```

## Note
It is no longer necessary to edit the file as we have provided command line arguments for the configuration. Please see below. 

# Run

## Source

```shell
$ sudo python3 dvpn_price.py --help
usage: dvpn_price.py [-h] [-t twap] [-p price] [-u user]

dVPN Price Oracle for dVPN Node operators v0.3.2

optional arguments:
  -h, --help            show this help message and exit
  -t twap, --twap twap  Time Weighted Average Price. --twap days
  -p price, --price price
                        Set the price per GB you would like to charge in USD.
                        i.e., --price 0.005
  -u user, --user user  Set the base directory where .sentinelnode/ exists
                        i.e., --user dvpn - implies (/home/dvpn/.sentinelnode)

```

Where **days** in `--twap` is the number of days to average a price over based on market price of the coin for each previous day. 

## Binary

```shell
$ sudo dvpn_price --help
usage: dvpn_price [-h] [-t twap] [-p price] [-u user]

dVPN Price Oracle for dVPN Node operators v0.3.2

optional arguments:
  -h, --help            show this help message and exit
  -t twap, --twap twap  Time Weighted Average Price. --twap days
  -p price, --price price
                        Set the price per GB you would like to charge in USD.
                        i.e., --price 0.005
  -u user, --user user  Set the base directory where .sentinelnode/ exists
                        i.e., --user dvpn - implies (/home/dvpn/.sentinelnode)

```


## Example
```shell
sudo dvpn_price --twap 10 --price 0.001 --user sentinel
```

This will average the price of *OSMO, SCRT, ATOM, DEC, DVPN* over the last 10 days. It will set a price of *$0.001/GB* and change the **config.toml** in the directory `/home/sentinel/.sentinelnode/config.toml`

## Cronjob
You can also create a cronjob (as root) to have this run every week, every month, every day, every hour, every minute. Just be sure to restart your node eventually for the changes to take place.

### Example
```shell
sudo crontab -e
```

Place the following line at the bottom of the file:
```
59 12 * * * /home/sentinel/Scripts/dvpn_price --twap 14 --price 0.003 --user sentinel
```

This will update your sentinel node **config.toml** every day at 12:59 p.m.

