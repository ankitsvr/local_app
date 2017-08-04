
import sys
import threading
import socket

def server_loop(local_host,local_port,remote_host,remote_port,recieve_first):
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind((local_host,local_port))

    except:
        print "failed to listen  on %s:%d " %(local_host,local_port)
        sys.exit()

    print "listening  on %s:%d" %(local_host,local_port)

    server.listen(5)

    while True:
        client_socket ,addr=server.accept()
        print "recieve incoming fom %s%d" %(addr[0],addr[1])

        proxy_thread=threading.Thread(target=proxy_handler,args=(client_socket,remote_host,remote_port,recieve_first))
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) !=5:
        print "usage"
        sys.exit(0)

    local_host=sys.argv(1)
    local_port=int(sys.argv[2])

    remote_host=sys.argv[3]
    remote_port=sys.argv[4]

    recieve_first=sys.argv[5]

    if "True" in recieve_first:
        recieve_first=True

    else:
        recieve_first=False

    server_loop(local_host,local_port,remote_host,remote_port,recieve_first)

main()
