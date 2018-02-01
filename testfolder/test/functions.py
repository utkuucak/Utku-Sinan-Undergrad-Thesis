import cv2
import numpy as np
def average_slope_intercept(lines):
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

def pixel_points(y1, y2, line):
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

def lane_lines(image, lines):
    """
    Create full lenght lines from pixel points.
        Parameters:
            image: The input test image.
            lines: The output lines from Hough Transform.
    """
    left_lane, right_lane = average_slope_intercept(lines)
    y1 = image.shape[0]
    y2 = y1 * 0.6
    left_line  = pixel_points(y1, y2, left_lane)
    right_line = pixel_points(y1, y2, right_lane)
    return left_line, right_line
    
def draw_lane_lines(image, lines, color=[0, 0, 255], thickness=13):
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
    
def draw_middle_line(image, lines, color=[0, 255, 0], thickness=13):
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
    return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)
    
def draw_position_line(image, color=[255, 0, 0], thickness=13):
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
    
    return cv2.addWeighted(image, 1.0, position_image, 1.0, 0.0)
