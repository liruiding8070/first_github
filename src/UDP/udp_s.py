import socket

pair = ('0.0.0.0', 9000)

sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sk.bind(pair)

while True:
    msg, addr = sk.recvfrom(1024)
    print('recv:', msg.decode('utf-8'), addr)
    sk.sendto(msg.upper(), addr)
