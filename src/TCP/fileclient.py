import socket
import os
import struct
from hashlib import md5


def get_md5(data):
    return md5(data.encode('utf-8')).hexdigest()


ip = '127.0.0.1'
port = 9000
sk = socket.socket(type = socket.SOCK_STREAM)
sk.connect((ip, port))

userName = input("UserName: ")
password = input("password: ")
md5code = get_md5(userName + password)
sk.sendall(md5code.encode('utf-8'))

fileSize = os.stat("1.jpg").st_size
print(fileSize)
header = struct.pack('i', fileSize)
sk.sendall(header)

sendSize = 0
with open("1.jpg", "rb") as f:  # read binary
    while sendSize < fileSize:
        data = f.read(1024)
        sk.sendall(data)
        sendSize += len(data)
sk.close
