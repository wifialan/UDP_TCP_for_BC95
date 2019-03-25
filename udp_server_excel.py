#coding=utf-8
import socket
import binascii
import string
import re
import sys
import os
import time
import struct
import xlwt

HOST = "0.0.0.0"
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)

dataCounter = 0

udpSerSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSerSock.bind(ADDR)

excelname = time.strftime("%Y-%m-%d-%H_%M_%S",time.localtime(time.time()))+'.xls'
workbook = xlwt.Workbook()
table = workbook.add_sheet(excelname) #excel 的文件名字
row = 0
colum = 0


while True:
        #print 'Waiting for message from BC95...'
        data, addr = udpSerSock.recvfrom(1024)
        readstr = str(binascii.b2a_hex(data))   #把接收到的数据转为字符型
        #BC95通过电信云接收的数据格式为2471e2e201ab4093，每四个字符为一组，第四组正好是压力数据
        sendData = re.findall(r'\w{1,4}',readstr)
        currenttime = time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()))
        #写入第一列序号数据
        table.write(row,0,str(row))
        #写入第二列时间数据
        table.write(row,1,currenttime)
        #写入第三列压力数据
        table.write(row,2,sendData[3])
        #保存数据
        workbook.save(excelname)
        #准备往下一行写入数据
        row = row + 1
        dataCounter = (dataCounter + 1) % 1024
        print 'Receive pressure data from BC95: ' + sendData[3]
        #print str(dataCounter)
        file = open("data.txt","w")                     #每打开一次文件，就把之前的数据给清空，保证txt文件中仅有最新的一个压力数据
        file.write(str(dataCounter) + '\n')     #写入数据次数
        file.write(sendData[3] )                #写入压力数据
        file.flush()

        file.close()
udpSerSock.close()
