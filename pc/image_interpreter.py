import cv2
import skvideo.io
import numpy as np
import time

class Image_Interpreter():
    def __init__(self,line_temp_left=None,line_temp_right=None,mid_line=((326,360),(331,144)),pos_line=((320,360),(320,180)),angle=1):
        self.line_temp_left=line_temp_left
        self.line_temp_right=line_temp_right
        self.mid_line=mid_line
        self.pos_line=pos_line
        self.angle=angle
        print("IN INIT METHOD")
    def average_slope_intercept(self,lines):
        """
        Find the slope and intercept of the left and right lanes of each image.
            Parameters:
                lines: The output lines from Hough Transform.
        """
        left_lines    = [] #(slope, intercept)
        left_weights  = [] #(length,)
        right_lines   = [] #(slope, intercept)
        right_weights = [] #(length,)

        for line in lines:
            for x1, y1, x2, y2 in line:
                if x1 == x2:
                    continue
                slope = (y2 - y1) / (x2 - x1)
                intercept = y1 - (slope * x1)
                length = np.sqrt(((y2 - y1) ** 2) + ((x2 - x1) ** 2))
                if slope < 0:
                    left_lines.append((slope, intercept))
                    left_weights.append((length))
                else:
                    right_lines.append((slope, intercept))
                    right_weights.append((length))
        left_lane  = np.dot(left_weights,  left_lines) / np.sum(left_weights)  if len(left_weights) > 0 else None
        right_lane = np.dot(right_weights, right_lines) / np.sum(right_weights) if len(right_weights) > 0 else None
        return left_lane, right_lane

    def pixel_points(self,y1, y2, line, eps=0.000001):
        """
        Converts the slope and intercept of each line into pixel points.
            Parameters:
                y1: y-value of the line's starting point.
                y2: y-value of the line's end point.
                line: The slope and intercept of the line.
        """
        if line is None:
            return None
        slope, intercept = line
        if slope==0:
            time.sleep(50)
        x1 = int((y1 - intercept)/(slope+eps))
        x2 = int((y2 - intercept)/(slope+eps))
        y1 = int(y1)
        y2 = int(y2)
        return ((x1, y1), (x2, y2))

    def lane_lines(self,image, lines):
        """
        Create full lenght lines from pixel points.
            Parameters:
                image: The input test image.
                lines: The output lines from Hough Transform.
        """
        #global line_temp_left
        #global line_temp_right
        left_lane, right_lane = self.average_slope_intercept(lines)
        y1 = image.shape[0]
        y2 = y1 * 0.4
        left_line  = self.pixel_points(y1, y2, left_lane)
        right_line = self.pixel_points(y1, y2, right_lane)
        if left_line is None or right_line is None:
            left_line= self.line_temp_left
            right_line= self.line_temp_right
            return left_line, right_line
        else:
            self.line_temp_left=left_line
            self.line_temp_right=right_line
            return left_line, right_line

    def draw_lane_lines(self,image, lines, color=[0, 0, 255], thickness=13):
        """
        Draw lines onto the input image.
            Parameters:
                image: The input test image.
                lines: The output lines from Hough Transform.
                color (Default = red): Line color.
                thickness (Default = 12): Line thickness.
        """
        line_image = np.zeros_like(image)
        for line in lines:
            if line is not None:
                if type(line) is not int:
                    cv2.line(line_image, *line,  color, thickness)
        return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)

    def draw_middle_line(self,image, lines, color=[0, 255, 0], thickness=13):
        """
        Draw middle line between road lanes.
            Parameters:
                image: The input test image.
                lines: The output lines from Hough Transform.
                color (Default = red): Line color.
                thickness (Default = 12): Line thickness.
        """
        line_image = np.zeros_like(image)
        for line in lines:
            if line is not None:
                #b=beginning e=end  l1b=line1beginningpoints
                (line1,line2)=lines
                (l1b,l1e)=line1
                (l2b,l2e)=line2
                (midxb,midyb)=((l1b[0]+l2b[0])//2,(l1b[1]+l2b[1])//2)
                (midxe,midye)=((l1e[0]+l2e[0])//2,(l1e[1]+l2e[1])//2)
                mid=((midxb,midyb),(midxe,midye))

                cv2.line(line_image, *mid,  color, thickness)
        return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0), mid

    def draw_position_line(self,image, color=[255, 0, 0], thickness=13):
        """
        Draw a line in the middle of the camera's view to track the car's
        current positon.
            Parameters:
                image: The input test image.
                color: Line color.
                thickness: Line thickness.
        """
        position_image = np.zeros_like(image)
        img_rows = image.shape[0]
        img_columns = image.shape[1]
        position_line = ((int(img_columns*0.5), img_rows),(int(img_columns*0.5), int(img_rows*0.5)))

        cv2.line(position_image, *position_line, color, thickness)

        return cv2.addWeighted(image, 1.0, position_image, 1.0, 0.0), position_line

    def find_angle(self, image, mid_line, pos_line, color=[255,255,255], thickness=5):
        """
        Calculates the angle between middle line and the position line.
        Prints the calculated angle on the frame.
            Parameters:
                image: The input test image.
                color: Text color
                thickness: Text thickness
        """
        angle_text = np.zeros_like(image)

        vector1 = ((mid_line[0][0]-mid_line[1][0]),(mid_line[0][1]-mid_line[1][1]))
        vector2 = ((pos_line[0][0]-pos_line[1][0]),(pos_line[0][1]-pos_line[1][1]))
        len1 = np.sqrt(vector1[0]**2 + vector1[1]**2)
        len2 = np.sqrt(vector2[0]**2 + vector2[1]**2)
        angle = np.arccos(np.dot(vector1, vector2)/(len1*len2)) # this is a number
        angle = str(round(angle * 180 / np.pi,2))
        angleAsFloat=float(angle)
        ((x1,y1),(x2,y2)) = mid_line
        if (x1 == x2):
            turn = 'straight'
        else:
            slope = (y2-y1)/(x2-x1)
            if (slope < 0):
                turn = 'right'
            else:
                turn = 'left'
                angleAsFloat = -angleAsFloat
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(angle_text, angle + turn, (30,45), font, 1, color, thickness, cv2.LINE_AA)
        return cv2.addWeighted(image, 1.0, angle_text, 1.0, 0.0),angleAsFloat
    def interprete_img(self):
        cap = skvideo.io.vread('../vids/pi_test_no_ps.mp4')
        length = int(cap.shape[0])
        car_cascade = cv2.CascadeClassifier('../train/cars.xml')
        for control, frame in enumerate(cap):
        # source image and copy of it
            src = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)
        
            src2 = np.copy(src)
            src2=cv2.blur(src2,(3,3))
            #ret,src2 = cv2.threshold(src2,45,255,cv2.THRESH_BINARY)
            #src4=np.copy(src2)
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
            # Hough line transform to find the lines in edge image
            linesP = cv2.HoughLinesP(masked_image,
                                     1, np.pi / 180, 50, None, 15, 10)
            #print(linesP)
            result = src2
#            mid_line=((326,360),(331,144))
#            pos_line=((320,360),(320,180))
#            angle=1
            if linesP is not None:
                for i in range(0, len(linesP)):
                    l = linesP[i][0]
                    cv2.line(src3, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)
            # Averaging and extrapolating the lines
                result = self.draw_lane_lines(src3, self.lane_lines(src, linesP))
                result, mid_line=self.draw_middle_line(result,self.lane_lines(src, linesP))
                result, pos_line=self.draw_position_line(result)
                result, angle = self.find_angle(result, mid_line, pos_line)
                print("mid: ",mid_line," Pos: ",pos_line," Angle: ",angle)
            # Drawing rectangle on cars which were found by HAAR Cascade
            for (x, y, w, h) in cars:
                cv2.rectangle(dst, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
            # Showing the result
            cv2.imshow('frame', result)
            #return  mid_line, pos_line, angle
            # Setting the result video frame break conditions
            if cv2.waitKey(1) & 0xFF == ord('q') or control == length:
                break
            #return  mid_line, pos_line, angle
        cv2.destroyAllWindows()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        