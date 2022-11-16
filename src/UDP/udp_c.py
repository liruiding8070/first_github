import socket

addr = ('127.0.0.1', 9000)  # '47.100.72.27'
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    msg = input("say: ")
    if not msg:
        break
    sk.sendto(msg.encode('utf-8'), addr)
    ser_msg, addr = sk.recvfrom(1024)
    print(ser_msg.decode('utf-8'))
