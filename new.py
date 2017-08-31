import signal
import socket
import threading
class Server():
    def __init__(self,config):


        self.serversocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.serversocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

        self.serversocket.bind((config['HOST_NAME'],config['BIND_PORT']))

        self.serversocket.listen(10)
        self.__client={}

        while True:
            clientSocket,client_address=self.serversocket.accept()
            d=threading.Thread(name=self.__getClientName(client_address),target=self.proxy_thread,args=(clientSocket,client_address))
            d.setDaemon(True)
            d.start()

        request=clientSocket.recv(config['MAX_REQUEST_LENGTH'])

        first_line=request.split('\n')[0]

        url=first_line.split(' ')[1]

        http_pos=url.find("://")

        if http_pos==-1:
            temp=url

        else:
            temp=url[(http_pos+3):]

        port_pos=temp.find(":")

        webserver_pos=temp.find("/")

        if webserver_pos==-1:
            webserver_pos=len(temp)

        webserver_pos=""

        port=-1

        if port_pos==-1 and webserver_pos<port_pos:
            port=80
            webserver=temp[:webserver_pos]


        else:
            port=int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])

            webserver=temp[:port_pos]


        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(config['CONNECTION_TIMEOUT'])
        s.connect((webserver,port))
        s.sendall(request)

        while 1:
            data=s.recv(config['MAX_REQUEST_LEN'])

            if len(data)>0:
                conn.send(data)

            else:
                break

