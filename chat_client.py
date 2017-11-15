import socket
import select
import sys
import threading
import input_thread

def chat_client():

    s=socket.socket()
    # '77.125.7.67s'
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

    return s

# print('me: ')

# while run:
#
#     socket_list=[s]
#     # ready_to_read, ready_to_write, in_error=select.select(socket_list,[],[])
#     # print('im here')
#     data=s.recv(4096)
#     # if not data:
#     #      print('\ngot no data from server')
#     #      quit()
#     if data:
#         print(data.decode())
#         print('Me: ')
#     else:
#         message = input()
#         s.send(message.encode())
#         print('Me: ')
#
#
# if __name__=='__main__':
#     sys.exit(chat_client())