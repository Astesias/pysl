import socket

# 创建socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取服务器的主机名和端口号
host = socket.gethostname()
port = 8888

# 连接到服务器
client_socket.connect((host, port))

# 发送消息给服务器
message = "Hello, 服务器!"
client_socket.send(message.encode())

# 接收服务器发送的响应数据
data = client_socket.recv(1024)

# 处理接收到的响应数据
print("接收到的数据为: ", data.decode())

# 关闭客户端连接
client_socket.close()
