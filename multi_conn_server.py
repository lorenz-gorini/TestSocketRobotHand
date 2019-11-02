import selectors
import socket
import types
import numpy as np
import random
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
IS_EXIT_COMMAND = 1    # To close the server
sel = selectors.DefaultSelector()  # This is the manager of the multi connections

def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print('accepted connection from', addr)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)


def close_socket(addr, sock, sel):
    print('closing connection to', addr)
    sel.unregister(sock)
    sock.close()


def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            close_socket(data.addr, sock, sel)

    if mask & selectors.EVENT_WRITE:
        msg = data.outb.decode()  # Decoding the message received by client
        if msg.lower() == "start":
            data_to_send = list(np.sin(np.arange(256)) + random.randint(0, 5))
            for d in data_to_send:
                d = f"{d}\r\n"
                sock.sendall(d.encode())   # Should be ready to write
                time.sleep(1 / 256.)
            print('sent a list',data_to_send[1], 'to', data.addr)

        if msg.lower() == "exit":   # If the message says "exit", the server will close itself
            return IS_EXIT_COMMAND
    return 0


def start_multi_conn_server():

    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.bind((HOST, PORT))
    lsock.listen()
    print('listening on', (HOST, PORT))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)

    close_connection = False  # to control the close command
    while not close_connection:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                response = service_connection(key, mask)
                if response == IS_EXIT_COMMAND:
                    close_connection = True


    sel.close()
    lsock.close()

if __name__ == "__main__":
    start_multi_conn_server()