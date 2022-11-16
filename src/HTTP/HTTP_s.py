import socket
from socket import SOL_SOCKET, SO_REUSEADDR

pair = ('0.0.0.0', 9000)
sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #
sk.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 重用端口
sk.bind(pair)
sk.listen(3)

text_content = b'''
HTTP/1.1 200 ok
Content-Type: text/html

<html>
<head></head>
<body>
    <h1>This is a picture</h1><br>
    <img src = "img.jpg" width="600"/>
</body>
</html>
'''

head = b'''
HTTP/1.1 200 ok
Content-Type: image/jpg

'''
with open('img.jpg', 'rb') as f:
    pic_content = head + f.read()

while True:
    conn, add = sk.accept()
    request = conn.recv(1024).decode('UTF-8')
    print("request: ", request)
    method = request.split(' ')[0]
    src = request.split(' ')[1]
    if method == "GET":
        if src == "/img.jpg":
            content = pic_content
        else:
            content = text_content
        conn.sendall(content)
    conn.close()
