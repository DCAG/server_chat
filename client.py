import socket

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server_ip=socket.gethostname()
port=9999
server_address=(server_ip,port)

s.connect(server_address)

user=input('what is your name? ')
data=user

s.sendall(data.encode())

data=s.recv(1024)
print(data.decode())
while True:
    data=input()
    s.sendall(data.encode())
    if data=='q':
        break
    data=s.recv(1024)
    print(data.decode())

s.close()

print('connection terminated by  the user (used \'q\')')

data='yo'
database2='yo'

