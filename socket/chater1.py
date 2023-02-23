import socket
import sys
import time
from threading import Thread

data=['0']
mes=['0']


def listen(s):
    if data:
        data[0] = s.recv(1024).decode()
        print('Received:', data[0])
    else:
        sys.exit(0)
    
    
def send(s):
    mes[0]=input()
    s.sendall(mes[0].encode())





#服务端主机IP地址和端口号
HOST = '10.20.85.35'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    #连接服务器
    s.connect((HOST, PORT))
except:
    print('Server not found or not open')
    sys.exit()
while True:
    t1=Thread(target=listen,args=(s,))
    t2=Thread(target=send,args=(s,))
    
    t1.start()
    t2.start()
    
    t1.join(1)
    t2.join(5)
    
    time.sleep(10)
#关闭连接
s.close()
