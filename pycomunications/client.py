import socket
import threading

def receive_and_print(c):
    while True:
        # data received from server
        data = c.recv(1024)
        if not data:
            print("Bye")
            break
        print('\nmessage received: ', str(data.decode('utf-8')))
        print('\n')

    # connection closed
    c.close()

# Create a socket object
s = socket.socket()

# Reserve a port on your computer
port = 52000

try:
    # Connect to the server
    s.connect(('127.0.0.1', port))

    # Receive data from the server
    print(s.recv(1024))
except Exception as e:
    print(e)
    # Close the connection
    s.close()
