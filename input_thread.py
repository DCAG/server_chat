import threading
from queue import Queue
import time
import platform
if platform.system() == 'Linux':
    import getch as ugetch
    LINE_ENDING = '\n'
elif platform.system() == 'Windows':
    import msvcrt as ugetch
    LINE_ENDING = '\r'    

os_type = platform.system()
getch=ugetch.getch
#getwch=ugetch.getwch

send_queue=Queue()
read_queue_buffer=Queue()
read_queue=Queue()
stop_threads=Queue()

class InputThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.sentence=[]
        self.paused=False
        self.paused_cond=threading.Condition()
        self.finished_sentence=False

    def pause(self):
        with self.paused_cond:
            self.paused_cond.wait(0.1)

    def resume(self):
        self.paused_cond.acquire()
        self.paused_cond.notify_all()
        self.paused_cond.release()

    def run(self):

        run=True

        while run:
            letter = getch()
            # checks for arrow keys - need to call getch twice otherwise --- crush
            if letter==b'\xe0':
                letter=getch()
                if os_type == 'windows':
                    letter=letter.decode()

                # placeholders for arrow keys functionality
                if letter=='K':
                    pass
                    # print('left arrow')
                if letter=='P':
                    pass
                    # print('down arrow')
                if letter=='H':
                    pass
                    # print('up arrow')
                if letter=='M':
                    pass
                    # print('right arrow')

                letter=''
            else:
                if os_type == 'Windows':
                    letter=letter.decode("utf-8", "ignore")
            if letter == LINE_ENDING:
                if len(self.sentence)>0:
                    temp=''.join(self.sentence)
                    send_queue.put(temp)

                    if temp=='quit':
                        run=False
                        # print('just stopped working')
                    else:
                        self.sentence=[]
                        self.finished_sentence=True
                        self.pause()
                        self.finished_sentence = False
                        # print('')
            elif letter=='\b':
                if len(self.sentence)>0:
                    self.sentence.pop()

            elif letter=='':
                pass
                # for bad characters, and undefined -- like arrow keys
                pass
            else:
                self.sentence.append(letter)
            time.sleep(0.01)
        return


def read(s):
    while True:
        # print('im in read thread')
        try:
            data=s.recv(4096)
            # print(data.decode())
            if data:
                data=data.decode()
                # print('\nis read_queue_buffer empty? ', read_queue_buffer.empty())
                # print('\nis read_queue empty? ', read_queue.empty())
                if read_queue_buffer.empty()==False:
                    start_of_sentence = read_queue_buffer.get()
                    sentence=data
                else:
                    # start of the message
                    start_of_sentence=''
                    sentence = data.split('*',3)
                    time_sent=sentence[0]
                    user=sentence[1]
                    length = int(sentence[2])
                    sentence=sentence[3]

                sentence=start_of_sentence+sentence

                if length>len(sentence):
                    read_queue_buffer.put(sentence)

                # middle of the message
                else:
                    while length==len(sentence) or length<len(sentence):
                        if length==len(sentence):
                            read_queue.put(time_sent+user+sentence)
                            sentence=''
                            if read_queue_buffer.empty() == False:
                                read_queue_buffer.get()
                        else:
                            if length<(len(sentence)):

                                read_queue.put(time_sent+ user + sentence[:length])
                                sentence=sentence[length:]
                                # so length will be taken when the loop comes again
                                sentence = sentence.split('*', 3)
                                if sentence[1]!='':
                                    user = sentence[1]
                                    time_sent=sentence[0]
                                length = int(sentence[2])
                                sentence = sentence[3]
                                if length>len(sentence):
                                    read_queue_buffer.put(sentence)

                # print(sentence)




                # read_queue.put(data.decode())
            else:
                print('\n<-Cant reach server->',end='')
                read_queue.put('')
                # time.sleep(5)
                break
        except Exception as e:
            # print(e)
            if stop_threads.empty()!=True:
                break
