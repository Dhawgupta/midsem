# coding: utf-8

# In[7]:


import socket
import os
import pwd
import random

sockComm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address1 = ('', random.randint(1024,20000))
address2 = ('', random.randint(1024,20000))

sockComm.bind(address1)
sockData.bind(address2)

sockComm.listen(4)
sockData.listen(4)
# s1 = socket.socket()
string = pwd.getpwuid(os.getuid())[0]  # 'dawg'#os.getlogin()
homeDir = "/home/" + string + "/"
os.chdir(homeDir)  # change to the home directory
# os.listdir('.')


# In[4]:


print("Server is Listening ...\nCommunication : {}\nData : {}".format(address1, address2))


def CWD(arg):
    pass


def RWD(arg):
    arg = arg.rstrip()
    print (arg)
    if os.path.exists("./" + arg):
        os.chdir("./" + arg)
        print ("Directory changed to {}".format(os.getcwd()))
        RETURN_CODE(101)  # directory changed successfully
    else:
        RETURN_CODE(-101)
        print("Directry not changed")
    # os.chdir('./' + arg)



def SEND(arg):
    # acknowledge the command with the resonse cde and then client will send the file
    RETURN_CODE(102)  # 102 to take the file
    # first line will contain the filename
    # from that onwards the data
    arg = arg.rstrip()
    filename =arg
    f = open(filename,'w')
    # data = s2.recv(1)
    # while data:
    #     f.write(data)
    #     data = s2.recv(1)
    data = s2.recv(4096)
    f.write(data)
    f.close()
    RETURN_CODE(103)
    print ("File Written")

def STORE(arg):

    arg = arg.rstrip()
    filename = arg
    if os.path.isfile(filename):
        RETURN_CODE(100) # send a positive code that file exsts
        f = open(filename,'rb')
        bit = f.read(1)
        data = ''
        while bit:
            data += bit
            bit = f.read()
        print ("The data to be sent is : \n{}".format(data))
        s2.sendall(data)

    else:
        RETURN_CODE(-100) # send code that 1file doesnt eist



def RETURN_CODE(code):
    # -100 is file not found
    # -101 is directory doenst exist
    message = str(code) + '\n'
    s1.sendall(message)


# In[ ]:


while True:
    s1, a1 = sockComm.accept()
    s2, a2 = sockData.accept()
    print("Recived Comm Connection from {} ".format(a1))
    print("Recived Data Connection from {} ".format(a2))
    while True:
        message = s1.recv(4096)
        cmd = message.split('\n')[0].split(' ')[0]
        arg = message.split('\n')[0].split(' ')[1]
        print ("Command : {} \nArgument: {}\n".format(cmd, arg))
        if cmd == 'cwd':
            CWD(arg)

        elif cmd == 'rwd':
            RWD(arg)
        elif cmd == 'send':
            SEND(arg)
        elif cmd == 'store':
            STORE(arg)
        else:
            print("Error")
            s1.close()
            s2.close()
            break



# In[ ]:


sockComm.close()
sockData.close()
