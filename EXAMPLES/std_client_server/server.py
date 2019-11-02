import socket
import time

import numpy as np
import random

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()

print('Connected by', addr)
close_connection = False
while not close_connection:
    data = list(np.sin(np.arange(256))+random.randint(0,5))
    for d in data:
        conn.send(str(d).encode())
        time.sleep(1/256.)
    time.sleep(1)
    try:
        client_response = s.recv(8192).decode()
        if client_response.lower() == "esc":
            close_connection = True
    except OSError:
        close_connection = False

conn.close()

s.close()
