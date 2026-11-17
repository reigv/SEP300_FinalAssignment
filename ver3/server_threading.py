import threading
import socket

host = '127.0.0.1'
port = 55559

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen()
server.settimeout(1.0) # accept() gives up every  1 s so ctrlC works 

clients = []
nicknames = []

def broadcast(message) :
    """Send a masg (bytes ) to every connected client"""
    for client in clients:
        try:
            client.send(message)
        except Exception:
            pass # client die!! its own handle() thread wiil clean it up

def handle(client):
    """Run in its own thread, one per client. listen and reply  msg"""
    while True:
        try: 
            message = client.recv(1024)
            if not message:
                break
            broadcast(message)
        except Exception:
            print('client hs died!')
            break  # connection err = as disconnect

    # clean up 
    if client in clients:
        index = clients.index(client)
        clients.pop(index)
        nickname = nicknames.pop(index)
        client.close()
        print(f'{nickname} gone!')
        broadcast(f'{nickname} left chat!'.encode('ascii'))

def receive():
    """Main loop: accept client forever"""
    while True:
        try:
            client, address = server.accept() # wait for new connection
        except socket.timeout:
            continue                # none join --> check again ( and let ctrlC)
        client.settimeout(None)     # client socket go back to normal blocking

        print(f'Connected with {address}')


        # handshake -- ask client for nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        # start new thread for this client so the main looop can go back to accepting 
        # daemon=True -- THREAD dies automaticlly when the main program exist
        thread = threading.Thread(target=handle, args=(client,), daemon=True)
        thread.start()

print('Server is running...')
try: 
    receive()
except KeyboardInterrupt:  # ctrlC
    print('Shutting Down')
    server.close()