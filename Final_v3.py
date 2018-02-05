import cv2
import skvideo.io
import numpy as np
from functions import Functions
import time

# Inheriting Functions
func = Functions()

# Capturing frames from video
cap = skvideo.io.vread('test_input.mp4')
length = int(cap.shape[0])

# Loading HAAR Cascade weight file
car_cascade = cv2.CascadeClassifier('cars.xml')

for control, frame in enumerate(cap):
    # source image and copy of it
    src = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)

    src2 = np.copy(src)

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
                             1, np.pi / 180, 50, None, 50, 10)

    # Averaging and extrapolating the lines
    result = func.draw_lane_lines(src2, func.lane_lines(src, linesP))

    # Drawing rectangle on cars which were found by HAAR Cascade
    for (x, y, w, h) in cars:
        cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Showing the result
    cv2.imshow('frame', result)

    # Setting the result video frame break conditions
    if cv2.waitKey(1) & 0xFF == ord('q') or control == length:
        break

cv2.destroyAllWindows()
