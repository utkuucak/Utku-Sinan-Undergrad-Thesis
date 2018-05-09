# A script to control the leds to light up with keyboard
# interactively. It will be used to drive the car manually

import RPi.GPIO as GPIO
import time
import pygame
from pygame.locals import *
import io
import picamera
from PIL import Image


PWM_frequency = 1000
full_throttle = 23.5
half_throttle = 30

left_pos = 19
left_neg = 21
left_en = 23

right_pos = 8
right_neg = 10
right_en = 12

p_left = 0
p_right = 0

#chan_list = [Forward, Back, Left, Right]
chan_list = [left_pos, left_neg, left_en, right_pos, right_neg, right_en]
#direction_list = [Forward, Back, Left, Right]


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(chan_list, GPIO.OUT)
    GPIO.output(chan_list, GPIO.LOW)
    pygame.init()
    pygame.display.set_mode((320,240))
    global p_left
    p_left = GPIO.PWM(left_en, PWM_frequency)
    global p_right 
    p_right = GPIO.PWM(right_en, PWM_frequency)
    p_left.start(0)
    p_right.start(0)
       
    #GPIO.output(Enable1, GPIO.HIGH)
    #GPIO.output(Enable2, GPIO.HIGH)
    

def destroy():
        GPIO.output(chan_list, GPIO.LOW)
        GPIO.cleanup()

def go_forward():
    GPIO.output([left_pos, right_pos], GPIO.HIGH)
    GPIO.output([left_neg, right_neg], GPIO.LOW)
    #p_left.ChangeDutyCycle(full_throttle)
    #p_right.ChangeDutyCycle(full_throttle)
    pwm_number = 0
    while(pwm_number <20.4):
        pwm_number = pwm_number+5
        p_left.ChangeDutyCycle(pwm_number)
        p_right.ChangeDutyCycle(pwm_number)
        time.sleep(0.005)


def go_reverse():
    GPIO.output([left_pos, right_pos], GPIO.LOW)
    GPIO.output([left_neg, right_neg], GPIO.HIGH)
    p_left.ChangeDutyCycle(full_throttle)
    p_right.ChangeDutyCycle(full_throttle)    

def steer_left():
    GPIO.output([left_neg, right_pos], GPIO.HIGH)
    GPIO.output([left_pos, right_neg], GPIO.LOW)
    p_left.ChangeDutyCycle(half_throttle)
    p_right.ChangeDutyCycle(half_throttle)    

def steer_right():
    GPIO.output([left_neg, right_pos], GPIO.LOW)
    GPIO.output([left_pos, right_neg], GPIO.HIGH)
    p_left.ChangeDutyCycle(half_throttle)
    p_right.ChangeDutyCycle(half_throttle)

#def steer_neutral():
    #GPIO.output([Right, Left], GPIO.LOW)

def forward_left():
    GPIO.output([left_pos, right_pos], GPIO.HIGH)
    GPIO.output([left_neg, right_neg], GPIO.LOW)
    p_left.ChangeDutyCycle(25)
    p_right.ChangeDutyCycle(0)

def forward_right():
    GPIO.output([left_pos, right_pos], GPIO.HIGH)
    GPIO.output([left_neg, right_neg], GPIO.LOW)
    p_left.ChangeDutyCycle(0)
    p_right.ChangeDutyCycle(25)

def back_left():
    GPIO.output([left_pos, right_pos], GPIO.LOW)
    GPIO.output([left_neg, right_neg], GPIO.HIGH)
    p_left.ChangeDutyCycle(half_throttle)
    p_right.ChangeDutyCycle(full_throttle)

def back_right():
    GPIO.output([left_pos, right_pos], GPIO.LOW)
    GPIO.output([left_neg, right_neg], GPIO.HIGH)
    p_left.ChangeDutyCycle(full_throttle)
    p_right.ChangeDutyCycle(half_throttle)

def go(Direction):
        GPIO.output(chan_list, GPIO.LOW)
        GPIO.output(Direction, GPIO.HIGH)

def stop():
        #GPIO.output(direction_list, GPIO.LOW)
        #p_left.ChangeDutyCycle(0)
        #p_right.ChangeDutyCycle(0)
        pwm_number = 30
        while( pwm_number > 0):
            pwm_number = pwm_number - 5
            p_left.ChangeDutyCycle(pwm_number)
            p_right.ChangeDutyCycle(pwm_number)
            time.sleep(0.005)

def interactive_train():
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.framerate = 5
        time.sleep(2) # warm up picam
        direction = ""
        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    key_input = pygame.key.get_pressed()

                    if key_input[pygame.K_w]:
                        print("Forward")
                        go_forward()
                        direction = "Forward"
                        
                    elif key_input[pygame.K_s]:
                        print("Reverse")
                        go_reverse()
                        direction = "Reverse"

                    elif key_input[pygame.K_j]:
                        print("Left")
                        steer_left()
                        direction = "Left"

                    elif key_input[pygame.K_k]:
                        print("Right")
                        steer_right()
                        direction = "Right"

                    elif key_input[pygame.K_q]:
                        print("Forward Left")
                        forward_left()
                        direction = "Forward-Left"

                    elif key_input[pygame.K_e]:
                        print("Forward Right")
                        forward_right()
                        direction = "Forward-Right"
                        
                    elif key_input[pygame.K_z]:
                        print("Back Left")
                        back_left()
                        direction = "Back-Left"

                    elif key_input[pygame.K_x]:
                        print("Back Right")
                        back_right()
                        direction = "Back-Right"

                    stream = io.BytesIO()
                    camera.capture(stream, format='jpeg', use_video_port=True)
                    stream.seek(0)
                    image = Image.open(stream)
                    image.save('image%s.jpg' % ("-" + direction + "-" + str(time.time())), format="JPEG")

                elif event.type == pygame.KEYUP:
                    print("Stop")
                    stop()


if __name__ == '__main__':
    setup()
    try:
        interactive_train()
    except KeyboardInterrupt:
        destroy()
