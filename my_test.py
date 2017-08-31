import socket
import signal

def serversocket(config):
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setsockopt()