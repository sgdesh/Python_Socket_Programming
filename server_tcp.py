# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:34:38 2020

@author: sgdes
"""

import socket
import tqdm
import os
import time

def send_file(client_socket,filename,BUFFER_SIZE):
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

SERVER_HOST = "127.0.0.1"
SERVER_PORT =12345
BUFFER_SIZE = 32*1024 #Initial buffer size. Do not change this
SEPARATOR = "_"

s = socket.socket()
s.bind((SERVER_HOST, SERVER_PORT))
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


client_socket, address = s.accept()
print(f"[+] {address} is connected.")
#progress=["A","B","C","D","E"]
t1=time.time()
#n = int(client_socket.recv(1).decode())
# for i in range(5):
#     filename=client_socket.recv(BUFFER_SIZE).decode()
#     send_file(client_socket,filename,BUFFER_SIZE)

while True:
    size=client_socket.recv(32).decode()
    if not size:
        break
    size=int(size)
    filename=client_socket.recv(32).decode()
    filesize= os.path.getsize(filename)
    #filesize_send = bin(filesize)[2:].zfill(32) 
    client_socket.send(f"{filesize}".encode())
   # print("Filesize sent")
    BUFFER_SIZE = 32*1024
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
s.close()