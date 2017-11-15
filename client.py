import time,sys
import threading
from queue import Queue
import msvcrt
import os
from input_thread import InputThread, read_queue, send_queue,read,stop_threads
from logging import debug
from chat_client import chat_client

os.system('cls')

s=chat_client()

print ('connected to '+str(s.getpeername())+'\n')



user=input('<-How do I call you?->\n<?>: ')
user=user.title()

print('\033[F]\033[F]\x1b[2K\r'+'<-How do I call you?->{-Fine-}', end='\n')
print('\x1b[2K\r<'+user+'>: ', end='')
s.sendall(user.encode())

input_t=InputThread()
input_t.start()

new_output=input_t.sentence
cur_output=[]


# print('\rMe: ',end='')
run=True
count = 0

read_t=threading.Thread(target=read,name='thread t',args=(s,))
read_t.start()

while run==True:
    new_output=''.join(input_t.sentence)

    if send_queue.empty()==False:
        message=send_queue.get()
        # print('\n'+message)
        length=len(message)
        mess=('*'+str(length)+'*'+message).encode()
        s.sendall(mess)

        if message=='quit':

            send_queue.put(message)
            stop_threads.put(0)
            run=False
            break
    while read_queue.empty()==False:
        message=read_queue.get()
        print('\x1b[2K\r' + message, end='\n')
        print('\r<'+user+'>: ' + new_output, end='')
    # else:
    #     try:
    #         data=s.recv(1024)
    #         print(data.decode())
    #     except:
    #         continue

    if len(cur_output)==len(new_output):
        time.sleep(0.01)
        pass
    else:
        print('\r<'+user+'>: '+new_output,end='')
        if len(cur_output)>len(new_output):

            # after the input thread gets a valid \n, it self pauses
            # in order to let the main use \n to go down a line while keeping in sync with server messages
            if input_t.finished_sentence==True:
                print('\n' + '\r<'+user+'>: ' + (new_output), end='')
                cur_output=[]
                input_t.resume()

            else:
                print('\x1b[2K\r' + '\r<'+user+'>: ' + (new_output), end='')
                cur_output=[]
        else:
            cur_output.append(0)
s.close()

print('\n<-Quit successful->\n')

print('<-A Chat->')
print('<-Made by <<Or S>>->')

quit()