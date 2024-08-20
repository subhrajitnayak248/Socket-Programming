import socket
import sys

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print('Socket created successfully!')

except socket.error as err:
    print(f'Socket creation failed with error {err}')


# gaieerror -> Problem with the DNS
port = 80 # HTTPS port
try:
    website = input('Enter the website: ')
    host_ip = socket.gethostbyname(website)

except socket.gaierror:
    print('Error resloving the host!')
    sys.exit()

# Connecting to the Server
s.connect((host_ip,port))
print(f'Socket has successfully connected to {website} of IP address {host_ip} on port {port}')
