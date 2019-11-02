# Echo client program
import socket
import sys

HOST = "127.0.0.1"        # The remote host
PORT = 50007              # The same port as used by the server
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)

s.sendall(b'Hello, world')
data = s.recv(8192)

print('Received', repr(data))

s.sendall(b'Hello, man')
data = s.recv(8192)

print('Received', repr(data))

s.sendall(b'Hello, ma2qwrEFn')
data = s.recv(8192)

print('Received', repr(data))