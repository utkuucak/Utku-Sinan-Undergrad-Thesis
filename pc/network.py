# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 00:55:43 2018

@author: Toshiba
"""

import socket
import socket
import sys
import cv2
import pickle
import numpy as np
import struct

class FrameReceiver:
    'This is the class for handling between Raspberry Pi and Server PC.'
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def getFrames(self):
        request = 'Send frame'

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # to reuse address
            print('Socket created')
        
            s.bind((HOST, PORT))
            print('Socket bind complete')
        
            # parameter is number of unaccepted connections before refusing
            s.listen(100) # new connections
            print('Socket now listening')
        
            # conn is a socket object used fo sending and receiving data
            # addr is the address of the connection from the other side
            conn, addr = s.accept()
        
            data = b""
            payload_size = struct.calcsize("I") # size of a struct with correspondin to I
            #print(payload_size)
            conn.send(bytes(request, "utf-8"))
            print('Request sent')
            while True:
        
                while len(data) < payload_size:
                    data += conn.recv(4096)
                    #data = conn.recv(4096)
                    packed_msg_size = data[:payload_size]
                    #print(packed_msg_size)
                    #print(np.shape(packed_msg_size))
                    data = data[payload_size:]
        
                    # result is a tuple even with one time thats why we need [0]
                    msg_size = struct.unpack("I", packed_msg_size)[0]
                    while len(data) < msg_size:
                        data += conn.recv(4096)
        
                    frame_data = data[:msg_size]
                    data = data[msg_size:] # remove the bytes moved to frame_data
        
                    print("Another frame received...")
                    frame = pickle.loads(frame_data)
    