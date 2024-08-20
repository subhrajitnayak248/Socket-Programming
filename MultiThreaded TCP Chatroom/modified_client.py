import threading
import socket

alias = input('Choose an alias: ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 59000

client.connect(('192.168.29.100', port))

def client_receive():
    """
    Function to receive messages from the server.
    
    This function runs in a separate thread, continuously listening for
    incoming messages from the server.
    """
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break

def client_send():
    """
    Function to send messages to the server.
    
    This function runs in a separate thread, continuously asking for user
    input and sending it to the server.
    """
    while True:
        message = input("")
        full_message = f'{alias} : {message}'
        client.send(full_message.encode('utf-8'))

# Start the receive thread
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

# Start the send thread
send_thread = threading.Thread(target=client_send)
send_thread.start()