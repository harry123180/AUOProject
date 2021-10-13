from random import randint

import socket

x = list(range(100))  # 100 time points


ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

Response = ClientSocket.recv(1024)
while True:
    #Input = input('Say Something: ')
    y = [str(randint(0, 100)) for _ in range(100)]  # 100 data points
    y = y[1:]  # Remove the first
    y.append(str(randint(0, 100)))  # Add a new random value.
    StrA = " ".join(y)
    ClientSocket.send(str.encode(StrA))
    Response = ClientSocket.recv(1024)
    print(Response.decode('utf-8'))

ClientSocket.close()