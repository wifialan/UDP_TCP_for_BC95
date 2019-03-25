#coding=utf-8

from socket import *
import time
import os
import string
import re

host = ''
port = 51314
bufsiz = 1024

ret = os.popen("netstat -nao|findstr " + str(port))
str_list = ret.read().decode('gbk')
ret_list = re.split('',str_list)
try:
    process_pid = list(ret_list[0].split())[-1]
    os.popen('taskkill /pid ' + str(process_pid) + ' /F')
    print "端口已被释放"
except:
    print "端口未被使用"


tcpSerSock = socket(AF_INET, SOCK_STREAM)  # 开启套接字
tcpSerSock.bind((host, port))  # 绑定服务端口
tcpSerSock.listen(5)  # 开始监听

judgedataflag = '0'
tcpSendFlag = 1

while True:
    while True:
        print 'Please waiting for connection...'
        tcpCliSock, addr = tcpSerSock.accept()
        print '...connected from:', addr
        tcpSendFlag = 1
        while tcpSendFlag:
            try:
                datafile = open("data.txt", "r")
                line = datafile.readlines()
                lines = len(line)
                #print 'There are ' + str(lines) + ' lines'
                if lines <=1:
                    #print 'There are ' + str(lines) + ' lines'
                    continue
                
                judgedata = line[0]  # 第一行为标志位，用于检测数据是否更新
                if judgedata != judgedataflag:  # 如果数据已经更新，则发送>数据，否则跳过不发送数据
                    judgedataflag = judgedata  # 更新标志位
                    predata = line[1]
                    print 'The data forwarded by TCP is: ' + predata
                    # data = tcpCliSock.recv(bufsiz)      # 接收客户端信息
                    # tcpCliSock.send("hell\n")
                    tcpCliSock.send(predata + '\n')
                    datafile.close()
                else:
		    time.sleep(0.2)#防止while空循环，造成CPU占用率飙升到100%
                    datafile.close()
            except IOError:
                print '----------------Losing connect!------------------'
                datafile.close()
                tcpSendFlag = 0
            except:
                print 'other factor--------------------'
                datafile.close()
                tcpSendFlag = 1
        tcpCliSock.close()
    tcpSerSock.close()
