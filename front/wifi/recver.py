import socket
from threading import Thread

def recvlink(client):
    while True:
        msg=client.recv(1024)
        print(msg.decode('utf-8'))

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host='192.168.111.240'
port=22

client.connect((host,port))
start_msg=client.recv(1024)

Thread(target=recvlink,args=(client,)).start()

