import base64

st = 'hello world!'.encode()#默认以utf8编码
res = base64.b64encode(st)
print(len(res.decode()))
print(res.decode())#默认以utf8解码
res = base64.b64decode(res)
print(res.decode())#默认以utf8解码
print(len(res.decode()))