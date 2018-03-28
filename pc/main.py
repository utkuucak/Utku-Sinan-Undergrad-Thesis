import cv2
import skvideo.io
import numpy as np
from functions import Functions

# Inheriting Functions
func = Functions()

# Capturing frames from video
#cap = skvideo.io.vread('../vids/test.mp4')
#cap = skvideo.io.vread('../vids/test2.mp4')
#cap = skvideo.io.vread('../vids/d2.mp4')
#cap = skvideo.io.vread('../vids/test_input.mp4')
#cap = skvideo.io.vread('../vids/test_input2.mp4')
cap = skvideo.io.vread('../vids/pi_test.mp4')
#cap = skvideo.io.vread('../vids/ttt.mp4')
length = int(cap.shape[0])

# Loading HAAR Cascade weight file
car_cascade = cv2.CascadeClassifier('../train/cars.xml')

for control, frame in enumerate(cap):
    # source image and copy of it
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
    bottom_left = [cols*0.10, rows*0.8]
    bottom_right = [cols*0.90, rows*0.8]
    top_left = [cols*0.35, rows*0.4]
    top_right = [cols*0.75, rows*0.4]
    roi_corners = np.array([[bottom_left, top_left, top_right,
                             bottom_right]], dtype=np.int32)
    channel_count = chan
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    masked_image = cv2.bitwise_and(dst, mask)
    pos= [int(cols*0.5), rows,int(cols*0.5), int(rows*0.5)]
    # Hough line transform to find the lines in edge image
    linesP = cv2.HoughLinesP(masked_image,
                             1, np.pi / 180, 50, None, 15, 10)
    if linesP is not None:
                for i in range(0, len(linesP)):
                    l = linesP[i][0]
                    cv2.line(src3, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
    # Averaging and extrapolating the lines
    result = func.draw_lane_lines(src3, func.lane_lines(src, linesP))
    result, mid_line=func.draw_middle_line(result,func.lane_lines(src, linesP))
    result, pos_line=func.draw_position_line(result)
    result = func.find_angle(result, mid_line, pos_line)
    # Drawing rectangle on cars which were found by HAAR Cascade
    for (x, y, w, h) in cars:
        cv2.rectangle(dst, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Showing the result
    cv2.imshow('frame', result)

    # Setting the result video frame break conditions
    if cv2.waitKey(1) & 0xFF == ord('q') or control == length:
        break

cv2.destroyAllWindows()
