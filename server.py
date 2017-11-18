import sys
import socket
import select
import datetime


def curr_time():
    now = datetime.datetime.now()
    minute=now.minute
    hour=now.hour
    if len(str(minute))<2:
        minute='0'+str(minute)
    else:
        minute=str(minute)
    if len(str(hour))<2:
        hour='0'+str(hour)
    else:
        hour=str(hour)

    now = ':'.join([hour, minute])
    now = now.join(['|', '|'])
    return now

host=''

port=9999

users_dict={}
SOCKET_LIST=[]
RECV_BUFFER=4096
leftovers=[]

def get_message(data):
    pass

def construct_message(user,data):
    now=curr_time()
    output = [now, user, str(len(data)), data]

    data = '*'.join(output)
    return data


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

                            data=' joined the chat]'
                            user='[' + users_dict[sock.getpeername()].title()

                            data=construct_message(user,data)

                            # data = (user+'*'+length+'*'+data).encode()
                            broadcast(sock, serversocket, data.encode())


                        else:
                            print(data.decode())

                            data = data.decode()
                            if data[-6:]=='4*quit':
                                data=(' left the chat]')
                                user = '[' + users_dict[sock.getpeername()].title()

                                data=construct_message(user, data)

                                SOCKET_LIST.remove(sock)
                                sock.close()
                                broadcast(sock, serversocket, data.encode())
                            else:

                                data=(curr_time()+'*'+'<'+users_dict[sock.getpeername()]+'>: '+data).encode()
                                broadcast(sock,serversocket,data)

                            # send the data to all users
                    else:
                        data = (' went offline]')
                        user = '[' + users_dict[sock.getpeername()].title()

                        data = construct_message(user, data)

                        print('no data')
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                        broadcast(sock, serversocket, data.encode())

                        # print to all that user is offline
                except Exception as e:
                    print(e)
                    # print(sock)
                    print('im in except with: '+users_dict[sock.getpeername()])

                    data = (' went offline]')
                    user = '[' + users_dict[sock.getpeername()].title()

                    data = construct_message(user, data)

                    broadcast(sock, serversocket,data.encode())
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