import threading
import socket
import time

port = 59000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.29.100', port))
server.listen()

# Lists to keep track of connected clients and their aliases
clients = []
aliases = []

# Dictionary to store blocked clients and their block expiration times
blocked_clients = {}

# List of abusive words that will trigger a block
abusive_words = ["fuck", "shit", "asshole", "bitch", "damn", "bastard"]

def broadcast(message, sender=None):
    """
    Send a message to all connected clients, except the sender.
    
    :param message: The message to broadcast
    :param sender: The client sending the message (to be excluded from broadcast)
    """
    for client in clients:
        if client != sender:
            client.send(message)

def client_handler(client):
    """
    Handle incoming messages from a client.
    
    This function runs in a separate thread for each connected client.
    It checks for abusive language and manages the blocking mechanism.
    """
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            
            # Check if the client is currently blocked
            if client in blocked_clients and time.time() < blocked_clients[client]:
                # If blocked, send a message to the client and continue the loop
                client.send("You are blocked for abusive language. Please wait.".encode('utf-8'))
            else:
                # If the client was blocked but the time has expired, remove from blocked_clients
                if client in blocked_clients:
                    del blocked_clients[client]
                
                # Check for abusive words in the message
                if any(word in message.lower() for word in abusive_words):
                    index = clients.index(client)
                    alias = aliases[index]
                    # Block the client for 5 minutes (300 seconds)
                    blocked_clients[client] = time.time() + 300
                    client.send("Warning: You have used abusive language. You are blocked for 5 minutes.".encode('utf-8'))
                else:
                    # If no abusive words, broadcast the message to all other clients
                    broadcast(message.encode('utf-8'), client)
        except:
            # Handle client disconnection
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat-room!'.encode('utf-8'))
            aliases.remove(alias)
            break

def receive():
    """
    Main function to accept new client connections.
    
    This function runs continuously, accepting new connections and starting
    a new thread for each connected client.
    """
    while True:
        print('Server is running and listening...')
        client, address = server.accept()
        print(f'Connection is established with {str(address)}')
        
        # Ask for the client's alias
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat-room'.encode('utf-8'))
        client.send('You are connected!'.encode('utf-8'))

        # Start a new thread to handle this client
        thread = threading.Thread(target=client_handler, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()