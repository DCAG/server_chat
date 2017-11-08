import sys
import socket
import select


host=''

port=9999


SOCKET_LIST=[]
RECV_BUFFER=4096

def chat_server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    serversocket.bind((host, port))

    serversocket.listen(10)

    SOCKET_LIST.append(serversocket)

    print('chat server started on port: ', port)
    run=True
    while run:
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST,[],[], 0)

        for sock in ready_to_read:
            if sock==serversocket:
                conn, address = sock.accept()
                SOCKET_LIST.append(conn)
                print(address, ' has connected to the server')
            else:
                try:
                    data=sock.recv(RECV_BUFFER)

                    if data:
                        if data=='q'.encode():
                            run=False
                        else:
                            broadcast(sock,serversocket,data)
                        # send the data to all users
                    else:
                        SOCKET_LIST.remove(sock)
                        broadcast(sock, serversocket, address+' went offline')

                        # print to all that user is offline
                except:
                    broadcast(sock, serversocket, address+' went offline')
                    # print to all that user is offline
                    continue
    serversocket.close()

def broadcast(sock, serversocket, data):

    for s in SOCKET_LIST:
        if s!=sock and s!=serversocket:
            try:
                s.send(data)
            except:
                s.close()
                if s in SOCKET_LIST:
                    SOCKET_LIST.remove(s)


if __name__=="__main__":
    sys.exit(chat_server())