import socket
import sys
import os
import time
host = sys.argv[2]
port = int(sys.argv[3])
filename = sys.argv[1]
data = open(filename, 'r')
file_size = os.stat(filename).st_size
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))
s.send(filename.encode())
answ = s.recv(1024)
if answ:
    print(f'Status received from server: {answ.decode()}')
    print("Initializing transfer...")
    chunk_size = 1024
    file_chunk = data.read(chunk_size).encode()
    sent = 0
    while(file_chunk):
        s.send(file_chunk)
        sent += chunk_size
        downloaded = int(sent*100/file_size)
        sys.stdout.write('\r\033[1;37;48m Downloaded: {}% {}{}'.format(downloaded, '\033[1;32;48m☻' * downloaded, '\033[0;34;48m☺' * (100 - downloaded)))
        sys.stdout.flush()
        time.sleep(0.05)
        file_chunk = data.read(chunk_size).encode()

s.close()
print('\033[0;37;48m\n')