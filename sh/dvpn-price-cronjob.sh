#!/bin/bash
#
# This will only work if you created a user name 'sentinel' with authorized ssh key access 
# from your running machine. 
#
# Also need 'sentinel ALL=(ALL:ALL) NOPASSWD: ALL' in /etc/sudoers
# This can be edited afterwards to remove the NOPASSWD permissions
#
# ssh pubkey access needs to be added to your /etc/ssh/sshd_config file
# for this to work
#

# EDIT THESE to all your IP ADDRESSES of your nodes
nodes=('usa.bluefren.xyz portugal.bluefren.xyz switzerland.bluefren.xyz finland.bluefren.xyz hongkong.bluefren.xyz')

# SSH PORT (EDIT)
port='22000'

# USERNAME OF DVPN NODE SOFTWARE
username='sentinel'
username2='v2ray'

# DVPN_PRICE VERSION
VERSION="v0.4.3"

for node in ${nodes[@]}; do
        echo "$node"

        ssh -p $port $username@$node << EOF
	wget -O - https://github.com/freQniK/dvpn_price/releases/download/$VERSION/dvpn_price_$VERSION.tar.gz | tar xvzf -
	sudo crontab -l > /home/$username/mycron
	echo " " > /home/$username/mycron
	echo "59 0 * * * /home/$username/bin/dvpn_price -t 5 -p 0.01 -q 0.005 -u $username" >> /home/$username/mycron
	echo "59 12 * * * /home/$username2/bin/dvpn_price -t 5 -p 0.01 -q 0.005 -u $username2" >> /home/$username/mycron
	if id "$username2" >/dev/null 2>&1; then
                sudo -H -u $username2 bash -c 'wget -O /home/$username2/dvpn.tar.gz https://github.com/freQniK/dvpn_price/releases/download/$VERSION/dvpn_price_$VERSION.tar.gz' && sudo -H -u $username2 bash -c 'tar xvzf /home/$username2/dvpn.tar.gz -C /home/$username2'
        else
                echo '$username2 not found'
        fi
        echo "Adding cronjob"
        sleep 2
        sudo crontab /home/$username/mycron
        sudo rm -rf /home/$username/mycron
EOF
done


