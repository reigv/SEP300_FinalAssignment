import socket
import threading

nickname = input('Your nickname : ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55559))

def receive():
    """Thread 1 -- constantly listen for messages from the server"""
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if not message:
                print('Disconnected to server!')
                break

            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except Exception:
            print('Disconnected!!')
            break
    client.close()


def write():
    """Thread 2 -- constantly wait for the user to type, then send"""
    while True:
        text = input("")
        if text == 'quit':
            client.close()
            break
        message = f'{nickname}: {text}'
        client.send(message.encode('ascii'))


# 2 thread -- receive && type(send) at the asme time
receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

write() # run write on the main thread, program ends when user types 'quit'