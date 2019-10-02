import socket
from threading import Thread
import os
import re

clients = []


class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name


    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        filename = self.sock.recv(1024).decode()
        print(f'Received filename {filename}')
        self.sock.send("OK".encode())
        fname, file_extension = os.path.splitext(filename)

        if os.path.exists(filename):
            files = [f for f in os.listdir('.') if re.match(r''+re.escape(fname)+r'_copy\d{1,}'+re.escape(file_extension), f)]
            max_ind = [re.findall( '\d{1,}',f) for f in files]
            if len(max_ind)>0:
                max_ind = max(list(map(int, max_ind[0])))
            else:
                max_ind=0
            filename = fname+f'_copy{max_ind + 1}'+file_extension
        file = open(filename, 'w')
        while True:
            data = self.sock.recv(1024)
            if data:
                file.write(data.decode())
            else:
                print(f'File received')
                self._close()
                return



next_name = 1
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 8800))
sock.listen()
while True:
    con, addr = sock.accept()
    clients.append(con)
    name = 'u' + str(next_name)
    next_name += 1
    print(str(addr) + ' connected as ' + name)
    ClientListener(name, con).start()



