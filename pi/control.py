# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 02:09:06 2018

@author: Toshiba
"""
import RPi.GPIO as GPIO
import time
import io

PWM_frequency = 1000

class Controller:
    def __init__(self):
        self.left_pos = 19
        self.left_neg = 21
        self.left_en = 23

        self.right_pos = 8
        self.right_neg = 10
        self.right_en = 12
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(chan_list, GPIO.OUT)
        GPIO.output(chan_list, GPIO.LOW)
        #global p_left
        self.p_left = GPIO.PWM(left_en, PWM_frequency)
        #global p_right 
        self.p_right = GPIO.PWM(right_en, PWM_frequency)
        self.p_left.start(0)
        self.p_right.start(0)
        
        self.chan_list = [left_pos, left_neg, left_en, right_pos, right_neg, right_en]
        
    def destroy(self):
        GPIO.output(self.chan_list, GPIO.LOW)
        GPIO.cleanup()
    