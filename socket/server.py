import socket

# 创建socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名和端口号
host = socket.gethostname()
port = 8888

# 将socket对象绑定到指定的主机和端口上
server_socket.bind((host, port))

# 开始监听连接
server_socket.listen(1)

# 等待客户端连接
print("等待客户端连接...")
client_socket, client_address = server_socket.accept()

print("连接来自: ", client_address)

# 接收客户端发送的数据
data = client_socket.recv(1024)

# 处理接收到的数据
print("接收到的数据为: ", data.decode())

# 发送响应数据给客户端
message = "欢迎连接到服务器!"
client_socket.send(message.encode())

# 关闭客户端连接
client_socket.close()
