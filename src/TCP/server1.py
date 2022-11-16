import socket
from socket import SOL_SOCKET, SO_REUSEADDR
from hashlib import md5
import threading


def get_md5(data):
    return md5(data.encode('utf-8')).hexdigest()


def chat(conn):
    while True:
        client_data = conn.recv(1024)
        if not client_data:
            break
        print(addr, ':', client_data.decode('utf-8'))
        content = input('>>> Reply: ').strip()
        conn.sendall(content.encode('utf-8'))  # .encode('utf-8')
    conn.close()


ip = '0.0.0.0'
port = 9000
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 实例化
sk.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
sk.bind((ip, port))  # 绑定
sk.listen(5)

db = {'xv': '1234', 'iot': '1234'}
dbcode = get_md5('iot' + db['iot'])
while True:
    conn, addr = sk.accept()
    print("Someone is coming...")
    print("client ip:", addr)
    thread = threading.Thread()
    thread.start()

    md5code = conn.recv(1024).decode('utf-8')
    if md5code == dbcode:
        print("You are a legal user~")
        conn.sendall('1'.encode('utf-8'))
        print('\033[0;32;40mWelcom to our bbs system!\033[0m')
        print('>>>' * 20)

        chat(conn)
    else:
        print('You are a illegal user~')
        conn.sendall('0'.encode('utf-8'))

sk.close()
