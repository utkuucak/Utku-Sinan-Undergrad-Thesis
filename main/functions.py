import cv2
import numpy as np
line_temp_left=0
line_temp_right=0
class Functions():
    def __init__(self):
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

    def pixel_points(self,y1, y2, line):
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
        x1 = int((y1 - intercept)/slope)
        x2 = int((y2 - intercept)/slope)
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
        global line_temp_left
        global line_temp_right
        left_lane, right_lane = self.average_slope_intercept(lines)
        y1 = image.shape[0]
        y2 = y1 * 0.4
        left_line  = self.pixel_points(y1, y2, left_lane)
        right_line = self.pixel_points(y1, y2, right_lane)
        if left_line is None or right_line is None:
            left_line= line_temp_left
            right_line= line_temp_right
        else:
            line_temp_left=left_line
            line_temp_right=right_line
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
        
        ((x1,y1),(x2,y2)) = mid_line
        if (x1 == x2):
            turn = 'straight'
        else:
            slope = (y2-y1)/(x2-x1)
            if (slope < 0):
                turn = 'right'    
            else:
                turn = 'left'
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(angle_text, angle + turn, (30,45), font, 1, color, thickness, cv2.LINE_AA)
        
        return cv2.addWeighted(image, 1.0, angle_text, 1.0, 0.0)      
