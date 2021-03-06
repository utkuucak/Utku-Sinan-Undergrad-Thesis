import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import time
import picamera
from picamera.array import PiRGBArray
from control import Controller
#cap = cv2.VideoCapture('../vids/test.mp4')
#cap.set(3,320)
#cap.set(4,240)
#time.sleep(2)
#cap.set(15, -8.0)

#cap.set(CV_CAP_PROP_FRAME_WIDTH,320)
#cap.set(CV_CAP_PROP_FRAME_HEIGHT,240)

cnt = Controller()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket, picamera.PiCamera() as camera :
    clientsocket.connect(('192.168.43.186', 8089))
    camera.resolution = (320, 240)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(320, 240))
    time.sleep(2)
    try:    # to release webcam with Ctrl + C
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True): 
        #while True:
            frame = frame.array
            incoming = clientsocket.recv(4096)
            incoming_str = str(incoming, "utf-8")
            if ('ANG' in incoming_str) or ('NLN' in incoming_str) or ('Send' in incoming_str):                      
                #ret, frame = cap.read()           
                data = pickle.dumps(frame)

                # clear buffer for next frame
                rawCapture.truncate(0)
                # 'I' means unsigned short
                # convert the length to a bytes object
                # concatenate the length data to frame and send it
                print("Sending frame...")
                clientsocket.sendall(struct.pack("I", len(data))+data) # ??
                #time.sleep(0.066)   # wait for 66 ms for 15fps
            if ('ANG' in incoming_str):
                angle = float(incoming_str[4:])
                print(str(angle))
                print(cnt.drive(angle))
    except KeyboardInterrupt:
#        cap.release()
        cv2.destroyAllWindows()
        cnt.destroy()
