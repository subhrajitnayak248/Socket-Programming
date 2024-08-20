# Socket Programming: 
# Server Socket listens on a Port at an IP, Client Socket connects to the Server

# Creating a Socket
import socket
import sys

# Creating a Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET -> Refers to address-family , SOCK_STREAM -> Connection-Oriented TCP
# In case of any error during creation of a socket as socket.error is thrown
# We can only connect to a server knowing it's IP address

# Getting IP address of a website -> ping www.website.com

# Getting IP address using Python -> socket.gethostbyname('website')
ip = socket.gethostbyname('www.google.com')
print(ip)


