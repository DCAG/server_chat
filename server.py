import sys
import socket
import select
import time




host=''

port=9999

users_dict={}
SOCKET_LIST=[]
RECV_BUFFER=4096
leftovers=[]

def get_message(data):
    pass


def chat_server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    serversocket.bind((host, port))

    serversocket.listen(10)

    SOCKET_LIST.append(serversocket)

    print('chat server started on port: ', port)
    run=True
    while run:
        ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST,[],[], 5)

        for sock in ready_to_read:
            if sock==serversocket:
                conn, address = sock.accept()
                SOCKET_LIST.append(conn)
                print(address, ' has connected to the server')
            else:
                try:

                    data=sock.recv(RECV_BUFFER)

                    if data:
                        # temp=True
                        # length=int(data.decode().split('*')[0])
                        # while len(data)<length:
                        #     data=sock.recv(RECV_BUFFER)
                        #
                        # if len(data)>length:
                        #
                        if sock.getpeername() not in users_dict:
                            users_dict[sock.getpeername()]=(data.decode()).title()
                            data = ('[' + users_dict[sock.getpeername()] + ' joined the chat]').encode()
                            broadcast(sock, serversocket, data)


                        else:
                            print(data.decode())

                            data = data.decode()
                            if data=='*4*quit':
                                data=('['+users_dict[sock.getpeername()]+' left the chat]').encode()
                                SOCKET_LIST.remove(sock)
                                sock.close()
                                broadcast(sock, serversocket, data)
                            else:
                                data=('<'+users_dict[sock.getpeername()]+'>: '+data).encode()
                                broadcast(sock,serversocket,data)

                            # send the data to all users
                    else:
                        data = ('['+users_dict[sock.getpeername()] + ' went offline]').encode()
                        print('no data')
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        broadcast(sock, serversocket, data)

                        # print to all that user is offline
                except Exception as e:
                    print(e)
                    print(sock)
                    print('im in except with: '+users_dict[sock.getpeername()])
                    data=(users_dict[sock.getpeername()]+' went offline').encode()
                    broadcast(sock, serversocket,data)
                    # if sock in ready_to_read:
                    #     ready_to_read.remove(sock)
                    sock.close()
                    if sock in SOCKET_LIST:
                        SOCKET_LIST.remove(sock)
                    # print to all that user is offline
                    continue

    serversocket.close()


def broadcast(sock, serversocket, data):

    for s in SOCKET_LIST:
        if s!=sock and s!=serversocket and (s.getpeername() in users_dict):
            try:
                print('im in broadcast')
                s.sendall(data)

            except Exception as e:
                print(e)
                print('im in broadcast closing: ',users_dict[s.getpeername()])
                if s in SOCKET_LIST:
                    SOCKET_LIST.remove(s)
                s.close()




if __name__=="__main__":
    sys.exit(chat_server())