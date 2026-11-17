import threading
import socket

host = '127.0.0.1' # local host || if on web pick ip of the server
port = 55559

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()  # put in listing mode for response

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try: # if this success --> broadcast to eveyone
            message = client.recv(1024)
            broadcast(message)
        except: # fail --> terminate
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            
            break
        # all thsi will run on thread, processing --> broadcast
        # terminate when client left

def receive():
    while True:
        client, address = server.accept()
        print(f'Connect with {str(address)}')

        # ask for chosen nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))

        client.send('Connect ot the server!!')

        thread = threading.Thread(target=handle, args=(client, ))
        thread.start()

print("Server is listening ...")
receive()