# A script to control the leds to light up with keyboard
# interactively. It will be used to drive the car manually

import RPi.GPIO as GPIO
import time
import pygame
from pygame.locals import *
import io
import picamera
from PIL import Image

Forward = 5
Back = 3
Enable1 = 7

Right = 8
Left = 10
Enable2 = 12

#chan_list = [Forward, Back, Left, Right]
chan_list = [Forward, Back, Enable1, Left, Right, Enable2]
direction_list = [Forward, Back, Left, Right]


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(chan_list, GPIO.OUT)
    GPIO.output(chan_list, GPIO.LOW)
    pygame.init()
    pygame.display.set_mode((320,240))
    GPIO.output(Enable1, GPIO.HIGH)
    GPIO.output(Enable2, GPIO.HIGH)

def destroy():
        GPIO.output(chan_list, GPIO.LOW)
        GPIO.cleanup()

def go_forward():
    GPIO.output(Forward, GPIO.HIGH)
    GPIO.output(Back, GPIO.LOW)

def go_reverse():
    GPIO.output(Back, GPIO.HIGH)
    GPIO.output(Forward, GPIO.LOW)

def steer_left():
    GPIO.output(Left, GPIO.HIGH)
    GPIO.output(Right, GPIO.LOW)

def steer_right():
    GPIO.output(Right, GPIO.HIGH)
    GPIO.output(Left, GPIO.LOW)

def steer_neutral():
    GPIO.output([Right, Left], GPIO.LOW)

def forward_left():
    GPIO.output([Forward, Left], GPIO.HIGH)
    GPIO.output([Back, Right], GPIO.LOW)

def forward_right():
    GPIO.output([Forward, Right], GPIO.HIGH)
    GPIO.output([Back, Left], GPIO.LOW)

def back_left():
    GPIO.output([Back, Left], GPIO.HIGH)
    GPIO.output([Forward, Right], GPIO.LOW)

def back_right():
    GPIO.output([Forward, Left], GPIO.LOW)
    GPIO.output([Back, Right], GPIO.HIGH)

def go(Direction):
        GPIO.output(chan_list, GPIO.LOW)
        GPIO.output(Direction, GPIO.HIGH)

def stop():
        GPIO.output(direction_list, GPIO.LOW)

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
                    image.save('image%s.jpg' % ("-" + direction + "-" + str(time.time())), formta="JPEG")

                elif event.type == pygame.KEYUP:
                    print("Stop")
                    stop()


if __name__ == '__main__':
    setup()
    try:
        interactive_train()
    except KeyboardInterrupt:
        destroy()
