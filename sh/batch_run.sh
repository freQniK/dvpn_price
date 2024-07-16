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

for node in ${nodes[@]}; do
        echo "------------------------------------$node------------------------------------"

        ssh -p $port $username@$node << EOF
        echo "Running dvpn_price as $username..."
	sudo /home/$username/bin/dvpn_price -t 5 -p 0.01 -q 0.005 -u $username
	if id "$username2" >/dev/null 2>&1; then
	        echo "Running dvpn_price as $username2..."
	        sudo /home/$username2/bin/dvpn_price -t 5 -p 0.01 -q 0.005 -u $username2
        fi
EOF
done

