import socket

#                       IPv4        &&     TCP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55559))
print(f"COnnect to server! Type 'quit' to exit")

while True:
    message = input('You: ')
    if message == 'quit': break

    client.send(message.encode('ascii'))

    # wait til server reply
    reply = client.recv(1024).decode('ascii')
    print(f'server: {reply}')



client.close()