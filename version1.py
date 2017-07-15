import socket
import sys
import threading
import getopt
import subprocess
from client_sender import *

listen=False
command=False
upload=False
execute=""
target=""
upload_destination=""
port=0


def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        print "no argument"

    try:
        opts,args=getopt.getopt(sys.argv[1:],"hle:t:cu:p",["help","listen","execute","target","command","upload"])

    except getopt.GetoptError as err:
        print str(err)


    for o,a in opts:
        if o in ("-h","--help"):
            print "no help"
        elif o in ("-l","--listen"):
            listen=True
        elif o in ("-e","--execute"):
            execute=a
        elif o in ("-c","--commandshell"):
            command=True
        elif o in ("-u","--upload"):
            upload_destination=a
        elif o in ("-t","--target"):
            target=a
        elif o in ("-p","--port"):
            port=int(a)
        else:
            assert False,"unhandled options"

    #are we going to listen or just  send data from stin?
    if not listen and len(target) or port > 0:
        buffer=sys.stdin.read()
        client_sender(buffer)

    if listen:
        server_loop()

main()
