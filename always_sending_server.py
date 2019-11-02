import socket
import numpy as np
import random
import time

host = '127.0.0.1'
port = 65432
buf = 1024

addr = (host, port)

# serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# # serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# serversocket.bind(addr)
# serversocket.listen(10)

clients = []
client_addresses = {}

def wait_for_new_client(serversocket):

    serversocket.listen()
    conn, client_address = serversocket.accept()
    print('Connected by', client_address)
    clients.append(conn)
    client_addresses[conn] = client_address

def close_client_conn(client):
    if client in clients:
        clients.remove(client)
        client.close()
        print("Closed connection by client ", client_addresses[client])

def push():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(addr)
    # The server will never close, or maybe with KeyboardInterrupt (TODO)
    while True:
        try:
            if len(clients):
                for c in clients:
                    data = list(np.sin(np.arange(256)) + random.randint(0, 5))
                    try:
                        for d in data:
                            c.send((str(d)+"\r\n").encode())
                            time.sleep(1 / 256.)
                    except OSError or ConnectionAbortedError:
                        close_client_conn(c)
                        continue
            else:
                wait_for_new_client(serversocket)
        except KeyboardInterrupt:
            serversocket.close()
            break


if __name__ == "__main__":
    push()