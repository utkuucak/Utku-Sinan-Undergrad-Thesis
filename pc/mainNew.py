from image_interpreter import Image_Interpreter
import cv2
import time
imi = Image_Interpreter()


mid,pos,angle=imi.interprete_img(cv2.imread('bb.jpg'))
print(mid," ",pos," ",angle)
#imi.interprete_img()
#print(imi.theAngle)
