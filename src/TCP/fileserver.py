import socket
import struct
from hashlib import md5
from tqdm import tqdm


def get_md5(data):
    return md5(data.encode('utf-8')).hexdigest()


ip = '0.0.0.0'
port = 9000
sk = socket.socket(type = socket.SOCK_STREAM)  # 套接字
sk.bind((ip, port))  # 绑定
sk.listen(5)
conn, addr = sk.accept()
db = {'xv': '1234', 'iot': '1234'}
dbmd5 = get_md5('iot' + db['iot'])

md5code = conn.recv(1024).decode('utf-8')
if md5code == dbmd5:

    # fileSize = conn.recv(1024).decode('utf-8')
    header = conn.recv(4)
    fileSize = struct.unpack('i', header)[0]
    print(fileSize)
    recvSize = 0

    pbar = tqdm(total = int(fileSize), desc = '下载进度')  # 添加进度条
    with open("a.jpg", "wb") as f:  # write binary
        while recvSize < int(fileSize):
            data = conn.recv(1024)
            f.write(data)
            recvSize += len(data)
            pbar.update(len(data))
            # print(f"received size: {recvSize} totle size: {fileSize}")
conn.close()
sk.close()
