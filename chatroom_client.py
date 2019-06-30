#!/usr/bin/env python3
#coding=utf-8
'''
name:George
email:276227382@qq.com
date:20190630
introduce:Chatroom client
env:python3.5
'''
from socket import *
import os,sys


def recv_msg(s):
    while True:
        data,addr = s.recvfrom(2048)
        if data.decode() == 'EXIT':
            sys.exit(0)
        print(data.decode() + '\n发表:',end='')

#发送消息
def send_msg(s,name,addr):
    while True:
        text = input("发表:")
        if text.strip() == 'quit':
            msg = 'Q '+ name
            s.sendto(msg.encode(),addr)
            sys.exit('退出聊天室')
            
        msg = 'C %s %s'%(name,text)
        s.sendto(msg.encode(),addr)

#创建套接字，登录，创建子进程
def main():
    if len(sys.argv) < 3:
        print('命令行输入有误')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST,PORT)

    #创建套接字
    s = socket(AF_INET,SOCK_DGRAM)

    while True:
        name = input('请输入姓名:')
        msg = 'L ' + name
        s.sendto(msg.encode(),ADDR)
        data,addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print('您已进入聊天室')
            break
        else:
            print(data.decode())

    pid = os.fork()
    if pid < 0:
        sys.exit('创建子进程失败')
    elif pid == 0:
        send_msg(s,name,ADDR)
    else:
        recv_msg(s)




    

if __name__ == '__main__':
    main()