# dvpn_price
Update Sentinel DVPN Node Prices with Market Changes

## Note 

This is for dVPN node versions 0.3.2

# Install
```shell
sudo apt install python3-pip
sudo pip install toml pycoingecko
```

Edit the lines in the python script that say **EDIT**
to your specifications.
Lines 9,10,15

# Run
```shell
sudo python3 dvpn_coin_conf.py
```

You can also create a cronjob (as root) to have this run every week, every month, every day, every hour, every minute. Just be sure to restart your node eventually for the changes to take place. 

