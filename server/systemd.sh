#!/bin/sh

config="./config.json"

config_name="config.json"
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
ExecStart=dugout $config_dir/$config_name

[Install]
WantedBy=multi-user.target
" > ${systemdfile}
chmod 644 ${systemdfile}
systemctl daemon-reload
systemctl enable dugout-server.service
systemctl start  dugout-server.service
systemctl status dugout-server.service
