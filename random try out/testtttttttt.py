# class Test(object):
#
#     def __init__(self):
#         self.a=[1]
#
#
# test=Test()
#
#
#
# b=test.a
#
# test.a[0]=5
#
# print(b)
#
# for i in range(5):
#     test.a[0]=8
#     print(b)
#
# print(b)
#
# x=2
# y=1
# try:
#     x=5
#     x=='2'
# except:
#     y=3
#
# print(y)

read_queue_buffer=[]
read_queue=[]
data='me:*6*jkp'
sentence = data.split('*',2)

# start of the message
user=sentence[0]
length = int(sentence[1])
# message=sentence[2]

print(sentence)

print(length)

stream=True

message='zxcme:*3*jkl'

read_queue_buffer.append('jkp')

if len(read_queue_buffer)!=0:
    first_data = read_queue_buffer.pop()
else:
    first_data=''
if length>len(message+first_data):
    read_queue_buffer.append(first_data+message)

    # second_data='zxcme:*3*jkl'

# middle of the message
elif length==len(message+first_data):
    read_queue.append(user+first_data+message)
    # print (read_queue)
elif length<(len(message)+len(first_data)):
    message=first_data+message
    read_queue.append(user + message[:length])
    message=message[length:]
    read_queue_buffer.append(message)
    start_of_message=True
    # print (message)

# temp=read_queue_buffer.pop()
# if length>len(message)+len(temp):
#     message=message+temp
# else:

print(read_queue.pop())


quit()