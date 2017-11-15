import msvcrt
import os
import sys
import time
import threading
global sentence
sentence=['Me: ']

os.system('cls')

getch=msvcrt.getch



def func1():
    while True:
        print('yo')
        time.sleep(1)
        print(threading.current_thread())

t=threading.Thread(target=func1,name='thread t')
t.start()
print(threading.current_thread())

# class Try(threading.Thread):
#
#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.temp=[]
#         self.paused=True
#         self.paused_cond=threading.Condition(threading.Lock())
#         self.finished_sentence=False
#
#     def pause(self):
#         self.paused=True
#
#         # self.paused_cond.acquire()
#
#     def resume(self):
#         self.paused_cond.acquire()
#
#         self.paused_cond.notify()
#         while True:
#             print('started sleep')
#             time.sleep(5)
#             print('stopped sleep')
#             break
#
#         self.paused_cond.release()
#     def run(self):
#
#         # with sentence_lock:
#         sentence=[]
#         for i in range (4):
#             self.temp=input('type your input: ')
#             sentence.append(self.temp)
#             self.temp=sentence
#             letter=0
#             print (len(sentence))
#             with self.paused_cond:
#                 self.paused_cond.wait()
#                 if len(sentence)==2:
#                     pass
#                     # self.pause()
#
#         print (sentence)
#
# t=Try()
#
# t.start()
#
# time.sleep(10)
# print('now program should resume')
#
#
# t.resume()
#
# t.paused=False
#
#
# print('\033[F]ok this should be a line up')