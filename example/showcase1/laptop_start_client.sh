#!/bin/bash
# cleanup
sudo iw dev mon3 del 2>/dev/null
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
sudo iw phy phy1 interface add mon2 type monitor
sleep 1
sudo ifconfig mon2 up
sleep 1
sudo iwconfig mon2 channel 9
sleep 1
sudo dumpcap -i mon2 -I -c 1
sleep 1
sudo iwconfig mon2 channel 36
sleep 1
sudo iw phy phy2 interface add mon3 type monitor
sleep 1
sudo ifconfig mon3 up
sleep 1
sudo iwconfig mon3 channel 9
sleep 1
sudo dumpcap -i mon3 -I -c 1
sleep 1
sudo iwconfig mon3 channel 36

#Create Client Interfaces
sudo iw phy phy1 interface add wifi2 type managed
sleep 1
sudo iw phy phy2 interface add wifi3 type managed
sleep 1
sudo ifconfig wifi3 192.168.3.203 netmask 255.255.255.0
sleep 1
sudo ifconfig wifi2 192.168.2.202 netmask 255.255.255.0
sleep 1
sudo iwconfig wifi2 essid effman-nuc2
sleep 1
sudo iwconfig wifi3 essid effman-nuc3 #
sleep 1
../../kdaemons.sh
