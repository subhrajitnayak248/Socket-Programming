import threading
import socket

alias = input('Choose an alias: ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 59000
# localhost = socket.gethostname()
# localhost_address = socket.gethostbyname(localhost)

# client.connect((localhost_address,59000))

client.connect(('192.168.29.100', port))

def client_receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if(message == "alias?"):
                client.send(alias.encode('utf-8'))
            
            else:
                print(message)
        except:
            print('Error!')
            client.close()
            break

def client_send():
    while True:
        message = f'{alias} : {input("")}'
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target = client_receive)
receive_thread.start()

send_thread = threading.Thread(target = client_send)
send_thread.start()











