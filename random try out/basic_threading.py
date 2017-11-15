import time,sys
from queue import Queue
import msvcrt
import os
from input_thread import InputThread, send_queue
from logging import debug


os.system('cls')

notification_example='important notification.! annoying...'

input_t=InputThread()
input_t.start()

new_output=input_t.sentence
cur_output=[]

notification=False

print('\rMe: ',end='')
run=True

while run==True:

    new_output=''.join(input_t.sentence)

    if send_queue.empty()==False:
        te=send_queue.get()
        if te=='quit':

            send_queue.put(te)
            run=False
            break

        else:
            send_queue.put(te)
    if notification==False:
        if len(cur_output)==len(new_output):
            pass
        else:
            print('\rMe: '+'\rMe: '+new_output,end='')
            if len(cur_output)>len(new_output):

                # after the input thread gets a valid \n, it self pauses
                # in order to let the main use \n to go down a line while keeping in sync with notifications
                if input_t.finished_sentence==True:
                    print('\n' + '\rMe: ' + (new_output), end='')
                    cur_output=[]
                    input_t.resume()

                else:
                    print('\x1b[2K\r' + '\rMe: ' + (new_output), end='')
                    cur_output=[]
            else:
                cur_output.append(0)
    elif notification==True:
        print('\x1b[2K\r'+'\rThis is a notification')
        print('Me: ',end='')
        print('\rMe: ' + (new_output), end='')
        notification=True

print(new_output)

print('sup???')

quit()