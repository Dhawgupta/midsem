# coding: utf-8

# In[7]:


import socket
import os
import pwd
import random
import sys

sockComm = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port1 = sys.argv[1]
port2 = sys.argv[2]
address1 = ('127.0.0.1', int(port1))
address2 = ('127.0.0.1', int(port2))

sockComm.connect(address1)
sockData.connect(address2)

# s1 = socket.socket()
string = pwd.getpwuid(os.getuid())[0]  # 'dawg'#os.getlogin()
homeDir = "/home/" + string + "/"
os.chdir(homeDir)  # change to the home directory
print ("PWD: {}".format(os.getcwd()))

# os.listdir('.')

print("Client up\nCommunication : {}\nData : {}".format(address1, address2))


while True:
    command = str(raw_input('>'))
    command = command.rstrip()
    cmd = command.split(' ')[0]
    args = command.split(' ')[1]
    arg = args.rstrip()
    print (cmd + ":" + arg)

    if cmd == 'cwd':
        if os.path.exists("./" + arg):
            os.chdir("./" + arg)
            print ("Directory changed to {}".format(os.getcwd()))

        else:
            print("Directory doesnt Exists :  not changed")
    elif cmd == 'rwd':
        sockComm.sendall(command)
        code = int(sockComm.recv(1024))
        if code == 101:
            print("Directory Changed")
        elif code == -101:
            print ("Directory not Changed")
        else:
            print("Unexpected Code {}".format(code))

    elif cmd == 'send':
        sockComm.sendall(command)
        ack = int(sockComm.recv(1024))
        if ack == 102:
            print("File acknowwledfe")
            f = open(arg,'rb')
            x = f.read(1)
            while x:
                sockData.send(x)
                x = f.read(1)
            f.close()
            ack = int(sockComm.recv(1024))
            if ack == 103:
                print("Transfer Complete ....")
            else:
                print ("Wrong Code {}".format(ack))
        else:
            print("Recieved {}".format(ack))


    elif cmd == 'store':
        sockComm.sendall(command)
        ack = int(sockComm.recv(1024))

        if ack == 100:
            f = open(arg,'wb')
            print("File Exists Begining Transfer")
            # f = open(arg, 'rb')
            x = sockData.recv(4096)
            f.write(x)
            #
            # x = sockData.recv(1)
            # while x:
            #     f.write(x)
            #     x = sockData.recv(1)
            #     # sockData.send(x)
            #     # x = f.read(1)
            f.close()
            print("Transfer Complete ....")
                # print ("Wrong Code {}".format(ack))
        elif ack == -100:
            print("FILE NOT FOUND")
        else:
            print("Unkown Code : {}".format(ack))

    else:
        print("Error Code Exiting")
        break


    # s1, a1 = sockComm.accept()
    # s2, a2 = sockData.accept()
    # print("Recived Comm Connection from {} ".format(a1))
    # print("Recived Data Connection from {} ".format(a2))
    # while True:
    #     message = s1.recv(4096)
    #     cmd = message.split('\n')[0].split(' ')[0]
    #     arg = message.split('\n')[0].split(' ')[1]
    #     print ("Command : {} \nArgument: {}\n".format(cmd, arg))
    #     if cmd == 'cwd':
    #         CWD(arg)
    #
    #     elif cmd == 'rwd':
    #         RWD(arg)
    #     elif cmd == 'send':
    #         SEND(arg)
    #     elif cmd == 'store':
    #         STORE(arg)
    #     else:
    #         print("Error")
    #         s1.close()
    #         s2.close()
    #         break



# In[ ]:


sockComm.close()
sockData.close()
