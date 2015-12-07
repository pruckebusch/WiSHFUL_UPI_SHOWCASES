#!/bin/bash

# cleanup
sudo iw dev mon2 del 2>/dev/null
sudo iw dev mon0 del 2>/dev/null
sudo iw dev mon1 del 2>/dev/null
sudo iw dev wlan0 del 2>/dev/null
sudo iw dev wlan1 del 2>/dev/null
sudo iw dev wlan2 del 2>/dev/null
sudo iw dev wlan3 del 2>/dev/null
sudo iw dev wlan4 del 2>/dev/null
sudo iw dev wlan5 del 2>/dev/null
sudo iw dev wlan6 del 2>/dev/null
sudo iw dev wifi0 del 2>/dev/null
sudo iw dev wifi2 del 2>/dev/null
sudo iw dev wifi3 del 2>/dev/null
sudo rfkill unblock all 2>/dev/null

#Creating Monitor Interface using Dumpcap Trick
sudo iw phy phy0 interface add mon2 type monitor
sleep 1
sudo ifconfig mon2 up
sleep 1
sudo iwconfig mon2 channel 9
sleep 1
sudo dumpcap -i mon2 -I -c 1
sleep 1
sudo iwconfig mon2 channel 36

#Configuring AP
sleep 1
../../kdaemons.sh
sleep 1
sudo killall -9 hostapd
sleep 1
sudo iw phy phy0 interface add wifi0 type managed
sleep 1
sudo ifconfig wifi0 192.168.2.102 netmask 255.255.255.0
sleep 1
sudo service network-manager stop
sleep 1
sudo hostapd hostapd-ch36-nuc2.conf &
