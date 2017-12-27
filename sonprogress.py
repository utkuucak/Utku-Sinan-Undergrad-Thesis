import sys
import math
import cv2
import numpy as np
import pygame
# I was changeddd
cap = cv2.VideoCapture(r'C:\Users\Sinan\Desktop\bitirme\d2.mp4')
car_cascade = cv2.CascadeClassifier('cars.xml')
while(cap.isOpened()):
      ret, frame = cap.read()
      if ret: 
            src = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
            src2=np.copy(src)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cars = car_cascade.detectMultiScale(
            gray,
            scaleFactor=1.13,
            minNeighbors=4,
            minSize=(25, 25))
            for (x,y,w,h) in cars:
                  cv2.rectangle(src2,(x,y),(x+w,y+h),(255,0,0),2)

                  
            dst = cv2.Canny(src, 350, 400, None, 3)
            
            [rows,cols,chan]=src.shape[:3]
            mask = np.zeros(dst.shape, dtype=np.uint8)
            bottom_left  = [cols*0.10, rows]
            bottom_right = [cols*0.90, rows]
            top_left     = [cols*0.45, rows*0.4]
            top_right    = [cols*0.50, rows*0.4]     
            roi_corners=np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
            channel_count = chan  # i.e. 3 or 4 depending on your image
            ignore_mask_color = (255,)*channel_count
            cv2.fillPoly(mask, roi_corners, ignore_mask_color)
            masked_image = cv2.bitwise_and(dst, mask)
            
            cdst = cv2.cvtColor(masked_image, cv2.COLOR_GRAY2BGR)
            cdstP = np.copy(cdst)
            cdstP2 = np.copy(cdstP)

            linesP = cv2.HoughLinesP(masked_image, 1, np.pi / 180, 50, None, 50, 10)

            if linesP is not None:
                for i in range(0, len(linesP)):
                    l = linesP[i][0]
                    cv2.line(src2, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

               


            # show the result
          
            cv2.imshow('frame',src2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                  break
cap.release()
cv2.destroyAllWindows()




