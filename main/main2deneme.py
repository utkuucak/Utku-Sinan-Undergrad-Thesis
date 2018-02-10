# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
#from functions import Functions

# Inheriting Functions
#func = Functions()

# Capturing frames 
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# Loading HAAR Cascade weight file
#car_cascade = cv2.CascadeClassifier('../train/cars.xml')
time.sleep(0.1)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    # source image and copy of it
    src = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

    src2 = np.copy(src)

    # obtaining the grayscale version of src for HAAR Cascade
    # and setting paramaters as well as detecting cars with it
    '''gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                        minNeighbors=8, minSize=(25, 25))
'''
    # Canny edge detection
    dst = cv2.Canny(src2, 100, 100, None, 3)

    # Defining a ROI
    [rows, cols, chan] = src2.shape[:3]
    mask = np.zeros(dst.shape, dtype=np.uint8)
    bottom_left = [0, rows]
    bottom_right = [cols, rows]
    top_left = [cols*0.20, rows*0.4]
    top_right = [cols*0.80, rows*0.4]
    roi_corners = np.array([[bottom_left, top_left, top_right,
                             bottom_right]], dtype=np.int32)
    channel_count = chan
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    masked_image = cv2.bitwise_and(dst, mask)

    # Hough line transform to find the lines in edge image
    linesP = cv2.HoughLinesP(masked_image,
                             1, np.pi / 180, 50, None, 50, 10)

    # Averaging and extrapolating the lines
    #result = func.draw_lane_lines(src2, func.lane_lines(src, linesP))
    #result, mid_line=func.draw_middle_line(result,func.lane_lines(src, linesP))
    #result, pos_line=func.draw_position_line(result)
    #result = func.find_angle(result, mid_line, pos_line)
    # Drawing rectangle on cars which were found by HAAR Cascade
#    for (x, y, w, h) in cars:
 #       cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Showing the result
    cv2.imshow('frame', dst)
    rawCapture.truncate(0)
    # Setting the result video frame break conditions
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
