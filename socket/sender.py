import socket
import sys
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.sendto(sys.argv[1].encode(),('10.20.87.35',5000))
s.close()

