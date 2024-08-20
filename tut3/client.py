import socket

s = socket.socket()
port = 56789

localhost = socket.gethostname()
localhost_ip = socket.gethostbyname(localhost)

s.connect((localhost_ip, port))
# 1024 -> Buffer Size
print(s.recv(1024))
s.close()

