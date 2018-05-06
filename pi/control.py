# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 02:09:06 2018

@author: Toshiba
"""
import RPi.GPIO as GPIO
import time
#import io


class Controller:
    def __init__(self):
        self.PWM_frequency = 1000
        
        self.left_pos = 19  # left motor positive pin
        self.left_neg = 21  # left motor negative pin
        self.left_en = 23   # left motor enable

        self.right_pos = 8  # right motor positive
        self.right_neg = 10 # right motor negative
        self.right_en = 12  # right motor enable
        
        self.left_speed = 0     # left pwm duty cycle
        self.right_speed = 0     # right pwm duty cycle
        
        self.chan_list = [self.left_pos, self.left_neg, self.left_en, self.right_pos, self.right_neg, self.right_en]
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.chan_list, GPIO.OUT)
        GPIO.output(self.chan_list, GPIO.LOW)
        GPIO.output([self.left_neg, self.right_neg], GPIO.HIGH)


        self.p_left = GPIO.PWM(self.left_en, self.PWM_frequency)
        self.p_right = GPIO.PWM(self.right_en, self.PWM_frequency)
        
        self.p_left.start(self.left_speed)
        self.p_right.start(self.right_speed)
        
        
        
    def destroy(self):
        GPIO.output(self.chan_list, GPIO.LOW)
        GPIO.cleanup()
        
    def drive (self, angle):
        if angle == angle: #check for Na #check for NaNN
           # angle = int(angle)
   
        # debug
            print('Angle: ' + str(angle))
            print( 'Right Speed: ' + str(self.right_speed))
            print('Left Speed: ' + str(self.left_speed))
            
            # when both pwm dc s are 0 and mid line and angle is found start driving
            if self.right_speed==0 and self.left_speed==0 and type(angle) is int:
                while self.right_speed < 25:
                    self.right_speed = self.right_speed + 5
                    self.left_speed = self.left_speed + 5
                    self.p_left.ChangeDutyCycle(self.left_speed)
                    self.p_right.ChangeDutyCycle(self.right_speed)
                    time.sleep(0.005)
                return "Driving started."        
            else:
                P =20.0
                change = angle/P
                self.right_speed = 23 + change
                self.left_speed = 23 - change
                self.p_right.ChangeDutyCycle(self.right_speed)
                self.p_left.ChangeDutyCycle(self.left_speed) 
                return("Driving.")
"""        elif abs(angle) <= 10:
            self.left_speed = dc_dict[angle][0]
            self.right_speed = dc_dict[angle][1]
             
            self.p_left.ChangeDutyCycle(self.left_speed)
            self.p_right.ChangeDutyCycle(self.right_speed)
            return ("Driving.")
"""            
#        elif angle>0 and abs(angle)<45: # turn right
#            pwm_change = int((angle/5) + 1)
#            self.left_speed += pwm_change
#            self.right_speed -= pwm_change
#            
#            if self.left_speed < 60:
#                self.p_left.ChangeDutyCycle(self.left_speed)
#            else: 
#                self.left_speed = 60
#                self.p_left.ChangeDutyCycle(self.left_speed) 
#                
#            if self.right_speed > 25:
#                self.p_right.ChangeDutyCycle(self.right_speed)
#            else:
#                self.right_speed = 25
#                self.p_right.ChangeDutyCycle(self.right_speed)
#            
#            return "Turning right."
#                
#        elif angle<0 and abs(angle)<45:
#            pwm_change = int((angle/5) + 1)
#            self.left_speed -= pwm_change
#            self.right_speed += pwm_change  
#            
#            if self.left_speed > 25:
#                self.p_left.ChangeDutyCycle(self.left_speed)
#            else: 
#                self.left_speed = 25
#                self.p_left.ChangeDutyCycle(self.left_speed) 
#                
#            if self.right_speed < 60:
#                self.p_right.ChangeDutyCycle(self.right_speed)
#            else:
#                self.right_speed = 60
#                self.p_right.ChangeDutyCycle(self.right_speed)
#                
#            return "Turning left."    
#        else:
#            return "Nothing is happening."
