
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

    local_host=sys.argv[1]
    local_port=int(sys.argv[2])

    remote_host=sys.argv[3]
    remote_port=int(sys.argv[4])

    recieve_first=sys.argv[5]

    if "True" in recieve_first:
        recieve_first=True

    else:
        recieve_first=False

    server_loop(local_host,local_port,remote_host,remote_port,recieve_first)


def proxy_handler(client_socket,remote_host,remote_port,recieve_first):
    #connect to remote socket

    remote_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))

    #recieve data from the remote end if necessary

    if recieve_first:
        remote_buffer=recieve_from(remote_socket)
        hexdump(remote_buffer)

        #send it out to response handler

        remote_buffer=response_handler(remote_buffer)

        if len(remote_buffer):
            print "====>sending to localhost  %s:%d " %len(remote_buffer)
            client_socket.send(remote_buffer)


    while True:
        local_buffer=recieve_from(client_socket)

        if len(local_buffer):
            print "===>receive %d byte from localhost." %len(local_buffer)
            hexdump(local_buffer)

            local_buffer=request_handler(local_buffer)


            remote_socket.send(local_buffer)
            print "===>sending to remote host"

        remote_buffer=recieve_from(remote_socket)

        if len(remote_buffer):
            print "===>recieve %d byte from remote host " %len(remote_buffer)
            hexdump(remote_buffer)

            # response handler
            remote_buffer=response_handler(remote_buffer)
            client_socket.send(remote_buffer)

            print "====>send to loaclhost"

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()

            print "====>no more data closing connection"

            break


def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
       s = src[i:i+length]
       hexa = b' '.join(["%0*X" % (digits, ord(x))  for x in s])
       text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.'  for x in s])
       result.append( b"%04X   %-*s   %s" % (i, length*(digits + 1), hexa, text) )
    return b'\n'.join(result)

def recieve_from(connection):
    buffer=""
    connection.settimeout(5)

    try:
        while True:
            data=connection.recv(4096)
            if not data:
                break

            buffer+=data

    except:
        pass
    return buffer

def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer

main()