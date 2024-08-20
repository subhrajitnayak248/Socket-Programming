import threading
import socket
import time

# Set the port number for the server
port = 59000

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to a specific IP and port
server.bind(('192.168.29.100', port))
# Listen for incoming connections
server.listen()

# Lists to store connected clients and their aliases
clients = []
aliases = []

# Dictionary to store blocked clients and their block expiration times
blocked_clients = {}
# Dictionary to store the last activity time for each client
last_activity = {}
# Dictionary to track if the first reminder has been sent to each client
first_reminder_sent = {}

# List of words considered abusive
abusive_words = ["fuck", "shit", "asshole", "bitch", "damn", "bastard"]

def broadcast(message, sender=None):
    """
    Send a message to all connected clients, except the sender.
    
    Args:
    message (bytes): The message to be broadcast
    sender (socket): The client socket that sent the message (to be excluded from broadcast)
    """
    for client in clients:
        if client != sender:
            client.send(message)

def check_inactivity(client):
    """
    Check if a client has been inactive and send reminders accordingly.
    
    Args:
    client (socket): The client socket to check for inactivity
    """
    while client in clients:
        current_time = time.time()
        # Calculate time since last activity
        time_since_last_activity = current_time - last_activity.get(client, current_time)
        
        # Check for first reminder (after 30 seconds)
        if not first_reminder_sent.get(client, False) and time_since_last_activity > 30:
            try:
                client.send("Hey there! Why don't you join the conversation?".encode('utf-8'))
                first_reminder_sent[client] = True
            except:
                break  # Exit if client disconnected
        # Check for subsequent reminders (every 3 minutes)
        elif first_reminder_sent.get(client, False) and time_since_last_activity > 180:
            try:
                client.send("It's been a while. Care to share your thoughts?".encode('utf-8'))
                # Reset the last activity time after sending the reminder
                last_activity[client] = current_time
            except:
                break  # Exit if client disconnected
        
        time.sleep(5)  # Wait for 5 seconds before next check

def client_handler(client):
    """
    Handle messages from a specific client.
    
    Args:
    client (socket): The client socket to handle
    """
    while True:
        try:
            # Receive message from client
            message = client.recv(1024).decode('utf-8')
            # Update the last activity time
            last_activity[client] = time.time()
            # Reset the first reminder flag
            first_reminder_sent[client] = False
            
            # Check if client is blocked
            if client in blocked_clients and time.time() < blocked_clients[client]:
                client.send("You are blocked for abusive language. Please wait.".encode('utf-8'))
            else:
                # Remove client from blocked list if block time has expired
                if client in blocked_clients:
                    del blocked_clients[client]
                
                # Check for abusive words
                if any(word in message.lower() for word in abusive_words):
                    index = clients.index(client)
                    alias = aliases[index]
                    # Block client for 5 minutes
                    blocked_clients[client] = time.time() + 300
                    client.send("Warning: You have used abusive language. You are blocked for 5 minutes.".encode('utf-8'))
                else:
                    # Broadcast the message if not abusive
                    broadcast(message.encode('utf-8'), client)
        except:
            # Handle client disconnection
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]
            broadcast(f'{alias} has left the chat-room!'.encode('utf-8'))
            aliases.remove(alias)
            # Clean up client data
            if client in last_activity:
                del last_activity[client]
            if client in first_reminder_sent:
                del first_reminder_sent[client]
            break

def receive():
    """
    Main function to accept new client connections and start handling threads.
    """
    while True:
        print('Server is running and listening...')
        # Accept new connection
        client, address = server.accept()
        print(f'Connection is established with {str(address)}')
        
        # Request and receive client's alias
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)
        
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat-room'.encode('utf-8'))
        client.send('You are connected!'.encode('utf-8'))

        # Initialize client data
        last_activity[client] = time.time()
        first_reminder_sent[client] = False

        # Start a thread to handle the client's messages
        thread = threading.Thread(target=client_handler, args=(client,))
        thread.start()

        # Start a thread to check for client inactivity
        inactivity_thread = threading.Thread(target=check_inactivity, args=(client,))
        inactivity_thread.start()

if __name__ == "__main__":
    receive()