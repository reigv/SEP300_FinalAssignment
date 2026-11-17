import socket

host = '127.0.0.1'
port = 55559

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                             AF_INET = IPv4 addr     SOCK_STREAM = TCP
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# let us reuse the port right after restarting --> avoid "addr already in use err"

server.bind((host, port)) # attach the socket to IP && PORT
server.listen() # --> start listening
print('server listening ...')

# accept() -- BLOCK! pause here until a client connects
# returns  --> a NEW socket jst
client, address = server.accept()
print(f'Connected with {address}')

while True:
    # recv() -- BLOXK til data arrive   and 1024 is the max byte to read at x1
    # data comes in as byte --> need decode() fuc --> str
    message = client.recv(1024).decode('ascii')

    # if msg is empty --> close connection
    if not message:
        print('CLient left')
        break
    print(f'CLient: {message}')

    reply = input("You: ") # server type a reply -- BLOCK til ENter
    client.send(reply.encode('ascii'))  # encode() str to bytes then send!

client.close() 
server.close()