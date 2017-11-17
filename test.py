# # from input_thread import p
# # from input_thread import getch
# # import unicodedata
# import msvcrt
#
# # getwch=msvcrt.getwch
# #
# # x=getwch()
#
# # try:
# #     x.decode()
# # except:
#
# data='helloquita'
#
# data=data[-5:]=='quit\''
# print(data)
# # print(x)
# # print(x.decode('unicode'))
#


# print('a', end='')
# print('a', end='')
# print('a', end='')
# print('a', end='')
# print('a', end='')
# print('a', end='')
# print('a', end='')
# print('a', end='')
# print('a', end='')

import win32gui
import time
# toplist = []
# winlist = []
# def enum_callback(hwnd, results):
#     winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
#
# win32gui.EnumWindows(enum_callback, toplist)
# firefox = [(hwnd, title) for hwnd, title in winlist if 'firefox' in title.lower()]
# # just grab the first window that matches
# firefox = firefox[0]
# # use the window handle to set focus
# win32gui.SetForegroundWindow(firefox[0])
w=win32gui.GetForegroundWindow()
# f=win32gui.GetForegroundWindow()
# w=win32gui.GetFocus()
while True:
    f = win32gui.GetForegroundWindow()
    if f==w:
        print('im in the same active window')
    if f!=w:
        print('im not currently focused')
    # win32gui.SetForegroundWindow(w)
    time.sleep(3)
quit()

