import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time
cap = cv2.VideoCapture(0)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
    clientsocket.connect(('localhost', 8089))
    try:    # to release webcam with Ctrl + C
        while True:
            incoming = clientsocket.recv(4096)
            if (str(incoming, "utf-8") == 'Send frame'):

                ret, frame = cap.read()
                data = pickle.dumps(frame)

                # 'I' means unsigned short
                # convert the length to a bytes object
                # concatenate the length data to frame and send it
                print("Sending frame...")
                clientsocket.sendall(struct.pack("I", len(data))+data) # ??
                #time.sleep(0.066)   # wait for 66 ms for 15fps
    except KeyboardInterrupt:
        cap.release()
        cv2.destroyAllWindows()
