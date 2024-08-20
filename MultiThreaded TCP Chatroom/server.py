' Chat-Room Connection - Client to Client'

import threading
import socket

# localhost = socket.gethostname()
# localhost_address = socket.gethostbyname(localhost)

port = 59000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.29.100', port))
server.listen()

clients = []
aliases = []

def broadcast(message):
    for client in clients:
        client.send(message)

def client_handler(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat-room!'.encode('utf-8'))
            aliases.remove(alias)
            break

# Main Function to receive client connections

def receive():
    while True:
        print('Server is running and listening...')
        client, address = server.accept()
        print(f'Connection is established with {str(address)}')
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat-room'.encode('utf-8'))
        client.send('You are connected!'.encode('utf-8'))

        thread = threading.Thread(target = client_handler, args =(client,))
        thread.start()

if __name__ == "__main__":
    receive()












