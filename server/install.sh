#!/bin/sh

python3 setup.py install || (echo "dugoutserver installation failed. Exiting" && exit 1)

config="./config.json"
config_name="server-config.json"
config_dir="/etc/dugout"
mkdir $config_dir
cp $config $config_dir/$config_name
systemdfile="/lib/systemd/system/dugout-server.service"
echo "
[Unit]
Description=Dugout Server
After=multi-user.target

[Service]
Type=idle
User=pi
ExecStart=/usr/local/bin/dugout-server $config_dir/$config_name -a 127.0.0.1

[Install]
WantedBy=multi-user.target
" > ${systemdfile}
chmod 644 ${systemdfile}

python3 -c "import pymodbus"
if [ "$?" -ne "0" ]; then # checks if pymodbus is missing and installs if this is the case
install_path="/tmp/dugout-install"
mkdir $install_path
cd $install_path || (echo "Entering temporal pymodbus installation failed. Exiting" && exit 1)
git clone https://github.com/abzicht/pymodbus -b Driver-Enable || (echo "Cloning pymodbus failed. Exiting" && exit 1)
cd $install_path/pymodbus || (echo "Entering pymodbus clone failed. Exiting" && exit 1)
python3 setup.py install || (echo "pymodbus installation failed. Exiting" && exit 1)
rm -rf $install_path
fi

systemctl daemon-reload
systemctl enable dugout-server.service
systemctl start  dugout-server.service
systemctl status dugout-server.service
