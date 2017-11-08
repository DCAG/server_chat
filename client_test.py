import socket
import select
import sys
def chat_client():

    s=socket.socket()

    host=socket.gethostname()
    port=9999
    server_address=(host,port)

    s.settimeout(2)
    run=True
    try:
        s.connect(server_address)
    except:
        print('unable to connect')
        quit()

    print('me: ')

    while run:
        socket_list=[sys.stdin, s]
        ready_to_read, ready_to_write, in_error=select.select(socket_list,[],[])

        for sock in ready_to_read:
            if s==sock:
                print('im here')
                data=sock.recv(4096)
                if not data:
                    print('\ndisconnected from chat server')
                    quit()
                else:
                    print(data)
                    print('Me: ')

            else:
                message=sys.stdin.readline()
                s.send(message)
                print('Me: ')


if __name__=='__main__':
    sys.exit(chat_client())