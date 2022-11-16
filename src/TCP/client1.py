import socket
from hashlib import md5


def get_md5(data):
    return md5(data.encode('utf-8')).hexdigest()


ip = '127.0.0.1'
port = 9000
sk = socket.socket()
sk.connect((ip, port))

userName = input('UserName: ')
password = input('password: ')
md5code = get_md5(userName + password)
sk.sendall(md5code.encode('utf-8'))
msg = sk.recv(1024)

if msg == b'1':
    print('You are a legal user~')
    while True:
        content = input('>>>Ask: ')
        sk.sendall(content.encode('utf-8'))
        server_msg = sk.recv(1024)
        print('\033[0;32;41mserver msg \033[0m', server_msg.decode('utf-8'))
    sk.close()
if msg == b'0':
    print('You are a illegal user~')
