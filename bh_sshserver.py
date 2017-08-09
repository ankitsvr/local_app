import socket
import threading
import paramiko
import sys

host_key=paramiko.RSAKey(filename="test_rsa.key")

class server(paramiko.ServerInterface):
    def __init__(self):
        self.event=threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if (username == 'root') and (password == "ankit"):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    server=sys.argv[1]
    port=int(sys.argv[2])

    try:
        sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock.bind(server,port)
        sock.listen(100)
        print '[+]Litening for connection...'

        client,addr=sock.accept()
    except Exception,e:
        print "listen failed: " +str(e)
        sys.exit()

    print "[+]Got a connection"


    try:
        bhSesssion=paramiko.Transport(client)
        bhSesssion.add_server_key(host_key)
        server=server()

        try:
            bhSesssion.start_server(server=server)

        except paramiko.SSHException,x:
            print"[-] ssh negotiation failed "


        chan=bhSesssion.accept(20)
        print "[+] Authenicated "

        print chan.recv(1024)

        chan.send("Welcome to ssh")

        while True:
            try:
                command=raw_input("enter command: ").strip('\n')
                if command !='exit':
                    chan.send(command)
                    print chan.recv(1024) +"\n"
                else:
                    chan.send('exit')
                    print 'exiting'
                    bhSesssion.close()
                    raise Exception('exit')
            except KeyboardInterrupt:
                bhSesssion.close()
    except Exception,e:
        print'[-] cauhght exception: '+str(e)

        try:
            bhSesssion.close()

        except:
            pass
        sys.exit(1)


