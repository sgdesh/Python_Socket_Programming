# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:34:38 2020

@author: sgdes
"""

import socket
import tqdm
import os
import time
from _thread import *
import threading 

lock1 =threading.Lock()

def send_file1(client_socket,filename,BUFFER_SIZE):
    filesize= os.path.getsize(filename)
    client_socket.send(f"{filesize}".encode())
    
    progress= tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break
            # s.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, True) # Uncooment this to disable delayed ACK=
            client_socket.send(bytes_read)
            progress.update(len(bytes_read))
#----------------------------------------------------
def sendfile(client_socket):
    while True:
        size=client_socket.recv(32).decode()
        if not size:
            lock1.release()
            break
        size=int(size)
        filename=client_socket.recv(32).decode()
        filesize= os.path.getsize(filename)
        #filesize_send = bin(filesize)[2:].zfill(32) 
        client_socket.send(f"{filesize}".encode())
       # print("Filesize sent")
   #     BUFFER_SIZE = 32*1024
        f=open(filename, 'rb')
        # filesize_remaining=filesize
        # while filesize_remaining>0:
        #     if filesize_remaining < BUFFER_SIZE:
        #         BUFFER_SIZE = filesize
        #     bytes_read = f.read(BUFFER_SIZE)
        #     client_socket.send(bytes_read)
        #     filesize_remaining=filesize_remaining-BUFFER_SIZE  
        # f.close()
        l=f.read()
        client_socket.sendall(l)    
        f.close()
        print(filename,"sent")
    
    client_socket.close()
#------------------------------------------------------------------------------    
SERVER_HOST = "127.0.0.1"
SERVER_PORT =12345
BUFFER_SIZE = 32*1024 #Initial buffer size. Do not change this
SEPARATOR = "_"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


while True:
   client_socket, address = s.accept()
   lock1.acquire()
   print("Successfully connected to client:", address )
   start_new_thread(sendfile, (client_socket,))  

s.close()


# def server():
#     i=1
#     while i<=10:
#         client_socket, address = s.accept()
#         pid_child=os.fork()
#         print(pid_child)
#         if pid_child==0:
#             print("Successfully connected to",i ," th client:", address )
#             sendfile(client_socket, address, i)
#             break
#         else:
#             i+=1

# server()            



s.close()