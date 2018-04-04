# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from functions import Functions

# Inheriting Functions
func = Functions()

# Capturing frames 
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 8
rawCapture = PiRGBArray(camera, size=(320, 240))
car_cascade = cv2.CascadeClassifier('../train/cars.xml')
time.sleep(0.5)
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    # source image and copy of it
    src = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
    src2 = np.copy(src)
    src2=cv2.blur(src2,(3,3))
    
    src3=np.copy(src)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                        minNeighbors=8, minSize=(25, 25))

    # Canny edge detection
    dst = cv2.Canny(src2, 100, 100, None, 3)

    # Defining a ROI
    [rows, cols, chan] = src2.shape[:3]
    mask = np.zeros(dst.shape, dtype=np.uint8)
    bottom_left = [cols*0.010, rows*0.8]
    bottom_right = [cols*0.99, rows*0.8]
    top_left = [cols*0.15, rows*0.4]
    top_right = [cols*0.85, rows*0.4]
    roi_corners = np.array([[bottom_left, top_left, top_right,
                             bottom_right]], dtype=np.int32)
    channel_count = chan
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    masked_image = cv2.bitwise_and(dst, mask)
    linesP = cv2.HoughLinesP(masked_image,
                             1, np.pi / 180, 50, None, 15, 10)
    #print(linesP)
    result = src2
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            #cv2.line(src3, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
    # Averaging and extrapolating the lines
        if cars is not None:
            func.Stop()
        result = func.draw_lane_lines(src3, func.lane_lines(src, linesP))
        result, mid_line=func.draw_middle_line(result,func.lane_lines(src, linesP))
        result, pos_line=func.draw_position_line(result)
        result = func.find_angle(result, mid_line, pos_line)
    # Showing the result
    cv2.imshow('frame', result)

    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
