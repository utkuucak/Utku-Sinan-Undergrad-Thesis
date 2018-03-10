import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import skvideo.io
from functions import Functions

# Inheriting Functions
func = Functions()

# Loading HAAR Cascade weight file
car_cascade = cv2.CascadeClassifier('../train/cars.xml')


HOST = ''
PORT = 8089

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

            src = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)

            src2 = np.copy(src)
            src2=cv2.blur(src2,(3,3))
            src3=np.copy(src)
            # obtaining the grayscale version of src for HAAR Cascade
            # and setting paramaters as well as detecting cars with it
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                                minNeighbors=8, minSize=(25, 25))

            # Canny edge detection
            dst = cv2.Canny(src2, 225, 225, None, 3)

            # Defining a ROI
            [rows, cols, chan] = src2.shape[:3]
            mask = np.zeros(dst.shape, dtype=np.uint8)
            bottom_left = [cols*0.10, rows]
            bottom_right = [cols*0.90, rows]
            top_left = [cols*0.35, rows*0.4]
            top_right = [cols*0.55, rows*0.4]
            roi_corners = np.array([[bottom_left, top_left, top_right,
                                     bottom_right]], dtype=np.int32)
            channel_count = chan
            ignore_mask_color = (255,)*channel_count
            cv2.fillPoly(mask, roi_corners, ignore_mask_color)
            masked_image = cv2.bitwise_and(dst, mask)

            # Hough line transform to find the lines in edge image
            linesP = cv2.HoughLinesP(masked_image,
                                     1, np.pi / 180, 50, None, 15, 10)
            if linesP is not None:
                        for i in range(0, len(linesP)):
                            l = linesP[i][0]
                            cv2.line(src3, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
            # Averaging and extrapolating the lines
            result = func.draw_lane_lines(src2, func.lane_lines(src, linesP))
            result, mid_line=func.draw_middle_line(result,func.lane_lines(src, linesP))
            result, pos_line=func.draw_position_line(result)
            result = func.find_angle(result, mid_line, pos_line)
            # Drawing rectangle on cars which were found by HAAR Cascade
            for (x, y, w, h) in cars:
                cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Showing the result
            cv2.imshow('frame', result)

            #cv2.imshow('frame', frame)

            cv2.waitKey(25)
            print('Finished with this frame.')
            #input('...')
            conn.send(bytes(request, "utf-8"))
            print('Request sent')
