"""
A module for sending a text file over network.

"""

import io
import socket
import struct
import time

HOST, PORT = "localhost", 9999

with open("./hotelCalifornia.txt", "r") as f:
    text = f.read()
    #print("File is read, contents:")
    #print(text)

# create socket and bind host
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))

    #print(text)

    sock.sendall(bytes(text, "utf-8"))


    # create a file like stram object for writing in text mode
    #connection = sock.makefile('w')
