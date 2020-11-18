# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 15:45:52 2020

@author: sgdes
"""

import socket
import tqdm
import os


def receive_file(filename,l,i):
    filesize=s.recv(BUFFER_SIZE).decode()
    filesize=int(filesize)
    filename=filename[:-4]+'_TCP_'+str(os.getpid())+'.txt'
    l[i] = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        
        for _ in l[i]:
            bytes_read = s.recv(BUFFER_SIZE)
            if not bytes_read:    
                break
            f.write(bytes_read)
            l[i].update(len(bytes_read))
#----------------------------------------------------------

SEPARATOR = "_"
BUFFER_SIZE = 32*1024 # Do not change this


host = "127.0.0.1"
port = 12345
#filesize = os.path.getsize(filename)

s = socket.socket()


print(f"[+] Connecting to {host}:{port}")
s.connect((host, port))
print("[+] Connected.")


file_arr=["War_and_Peace.txt","Beowulf.txt","Dracula.txt","Moby_Dick.txt","Sherlock Holmes.txt" ]
#n=len(file_arr)
#s.send(f"{n}".encode())
l=["A","B","C","D","E"]

for filename in file_arr:
    size=len(filename)
    size = bin(size)[2:].zfill(32) # encode filename size as 16 bit binary
    s.send((size).encode())
    s.send((filename).encode())
    filesize=s.recv(BUFFER_SIZE).decode()
    filesize=int(filesize)
    
    filename1=filename[:-4]+'_TCP_'+str(os.getpid())+'.txt'
    f= open(filename1, 'wb')
    BUFFER_SIZE = 32*1024
    filesize_remaining=filesize
    while filesize_remaining>0:
        if filesize_remaining < BUFFER_SIZE:
            BUFFER_SIZE = filesize
        bytes_read = s.recv(BUFFER_SIZE)
        filesize_remaining=filesize_remaining-BUFFER_SIZE
        f.write(bytes_read)
    f.close()
    print(filename,"received")
    
    #s.send(f"{filename}".encode())
    #receive_file(filename,l)
    #i+=1
s.close()