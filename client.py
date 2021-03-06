import time,datetime
import threading
import os
import platform
from input_thread import InputThread, read_queue, send_queue,read,stop_threads
from chat_client import chat_client


os_type = platform.system()

if os_type == 'Linux':
    clearscreen_command = 'clear'
elif os_type == 'Windows':
    import winsound
    import win32gui
    clearscreen_command = 'cls'
    this_window=win32gui.GetForegroundWindow()
else:
    print('this is the system platform.system found'+os_type)
    print('error: cannot figure out what system youre using')
    print('exiting program')
    clearscreen_command=''
    stop_threads.put(True)
    quit()

def play_sound(filename):
    if not os_type == 'Windows':
        return False
    
    filepath=os.path.join(BASE_DIR,filename)
    os.system('powershell -c (New-Object Media.SoundPlayer '+filepath+').PlaySync();')



def is_window_focused(this_window):
    if not os_type == 'Windows':
        return False
    f = win32gui.GetForegroundWindow()
    if f == this_window:
        return True
    if f != this_window:
        return False


os.system(str(clearscreen_command))

BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))


s=chat_client()

print ('Connected to '+str(s.getpeername())+'')

print('<<-To exit type: quit->>\n')

user=input('<-How do I call you?->\n<?>: ')
user=user.title()

print('\033[F]\033[F]\x1b[2K\r'+'<-How do I call you?->{-Fine-}', end='\n')
print('\x1b[2K\r<'+user+'>: ', end='')

s.sendall(user.encode())

input_t=InputThread()
input_t.start()

new_output=input_t.sentence
cur_output_length=0


# print('\rMe: ',end='')
run=True
count = 0

read_t=threading.Thread(target=read,name='thread t',args=(s,))
read_t.start()

notified=False
notify_timer=0
while run==True:
    new_output=''.join(input_t.sentence)
    if len(new_output)!=0:
        cur_output=new_output
    if send_queue.empty()==False:
        message=send_queue.get()
        # print('\n'+message)
        length=len(message)
        mess=('*'+str(length)+'*'+message).encode()
        try:
            s.sendall(mess)
        except:
            print('\n<-Cant reach server->',end='')

        if message=='quit':

            send_queue.put(message)
            stop_threads.put(0)
            run=False
            break
    while read_queue.empty()==False:
        # now=' -'+now
        # now=now.join(['<','>'])
        # print('<-' + str(now.hour) + ':' + str(now.minute) + '->')
        message=read_queue.get()
        print('\x1b[2K\r'+ message, end='\n')
        print('\r<'+user+'>: ' + new_output, end='')
        if os_type == 'Windows':
            if is_window_focused(this_window):
                notified=False
                # play_sound('DragonBallImpact.wav')
            elif notified==False:
                play_sound('DonorCardAppears.wav')
                notify_timer=time.time()
                notified=True
            elif notify_timer+60>time.time():
                notified=False
    # else:
    #     try:
    #         data=s.recv(1024)
    #         print(data.decode())
    #     except:
    #         continue

    if cur_output_length==len(new_output):
        time.sleep(0.01)
        pass
    else:
        # print('\r<'+user+'>: '+new_output,end='')
        # cur_output_length > len(new_output)
        # print(str(cur_output_length)+' '+str(len(new_output)))
        #
        # if ((cur_output_length)<(len(new_output))):
        #     print('fucking Heeeeellll')

        if cur_output_length>len(new_output):

            # after the input thread gets a valid \n, it self pauses
            # in order to let the main use \n to go down a line while keeping in sync with server messages
            if input_t.finished_sentence==True:
                while cur_output_length>0:
                    print('\b',end='')
                    cur_output_length-=1

                now = datetime.datetime.now()
                now = ':'.join([str(now.hour), str(now.minute)])
                now = now.join(['|','|'])
                print('\r'+now+'<' + user + '>: ' + cur_output, end='')

                print('\n' + '\r<'+user+'>: ' + (new_output), end='')
                cur_output_length=0
                input_t.resume()

            else:
                while cur_output_length>len(new_output):
                    print('\b \b',flush=True,end='')
                # print('\x1b[2K\r' + '\r<'+user+'>: ' + (new_output), end='')
                    cur_output_length-=1

        elif cur_output_length<len(new_output):
            print(new_output[cur_output_length:],flush=True,end='')
            cur_output_length = len(new_output)
s.close()


print('\n<-Quit successful->\n')

print('<-A Chat->')
print('<-Made by <<Or S>>->')

time.sleep(2)

quit()