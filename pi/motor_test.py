# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from motor_driver import Motors
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 5
rawCapture = PiRGBArray(camera, size=(320, 240))
mot = Motors()
mot.set_gpio_pins()
pwm = mot.get_pwm_imstance()
mot.start_pwm(pwm)
mot.set_idle_mode()
# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	
	
	'''
        MOTOR CONTROL
        '''
	#mot.set_forward_mode()
	mot.set_reverse_mode()
	#mot.set_right_mode()
	mot.set_left_mode()
	
	
	
	image = frame.array
        #
	# show the frame
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
       
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
        
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
                mot.set_idle_mode()
                break