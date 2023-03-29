#服务器端
import socket
from threading import Thread


def recv_msg(clientsocket):
    while True:
        recv_msg = clientsocket.recv(10240)
        print(recv_msg.decode('utf-8'))


socket_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host='0.0.0.0'
port=22

socket_server.bind((host,port))
socket_server.listen(2)

clientsocket,addr=socket_server.accept()

clientsocket.send('你现在已经连接上了服务器啦，我们来聊天吧！'.encode('utf-8'))

Thread(target=recv_msg,args=(clientsocket,)).start()

'''
    # 发送消息
    while True:
        reply="cer"
        clientsocket.send(reply.encode('utf-8'))
    clientsocket.close()
'''
