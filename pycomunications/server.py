import socket
import threading

def receive_and_print(c):
    while True:
        # Data received from client
        data = c.recv(1024)
        if not data:
            print("Bye")
            break
        print('\nmessage received: ', data.decode('utf-8'))

    # connection closed
    c.close()

def Main():
    # Create a socket object and bind the to peers
    host = "0.0.0.0"
    port = 52000

    s = socket.socket()
    s.bind((host, port))
    print('socket binded to port', port)

    s.listen(5)
    print('socket is listening')

    # a forever loop until the client exit
    try:
        while True:
            # establish connection with client
            c, addr = s.accept()

            # Start a new thread
            t = threading.Thread(target=receive_and_print, args=(c,))
            t.start()

            while True:
                text = input("\n")
                c.send(text.encode('utf-8'))
    except Exception as e:
        print(e)
    # Close the connection
    s.close()

if __name__ == '__main__':
    Main()

# Create a socket object
s = socket.socket()

# Reserve a port on your computer
port = 52000

# Bind to the listener to Local Area Network
s.bind(('0.0.0.0', port))

# Put the socket into listening mode
s.listen(5)

# run the server forever until interruption
try:
    while True:
        # Establish connection with client
        c, addr = s.accept()
        c.send(b"Hello, I am the server")
except Exception as e:
    print(e)
    s.close()
    c.close()
    print("Server closed")