import socket

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(1)
conn, addr = sock.accept()

print 'connected:', addr

# f = open('test.json', 'w')
while True:
    data = conn.recv(1024)
    f.write(data)
    if not data:
        conn.send('file recieved')
        break
conn.close()
f = open('test.json', 'w')
f.write(data)
f.close()
print 'file received'
