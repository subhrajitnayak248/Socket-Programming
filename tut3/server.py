# bind() -> Binds the socket to a specific IP and port so it can listen to incoming requests
# listen() -> Puts the server to a listen mode which allows the server to listen to incoming requests
# accept() -> Initates a connection to a client
# close() -> Closes a connection to a client

import socket

s = socket.socket()
print("Socket created successfully!")

port  = 56789

# bind(('IP_ADDRESS',PORT)) -> Here the IP is left empty so server can listen to other requests from other computers on the network
s.bind(('',port))
print(f'Socket binded to port: {port}')

# listen(Max_no_of_Connections)
s.listen(5) # Maximum 5 connections are possible and 6th connection will be refused
print('Socket is listening!')

while(True):
    c, addr = s.accept() # c -> connection, addr -> IP address
    print(c)
    print(f'Connected to {addr}')
    message = ('Thank you for connecting...')

    # send() -> Sends message in form of bytes 
    # encode() -> Converts the String to bytes
    c.send(message.encode())

    c.close()


    





