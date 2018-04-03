# Blinks all PIN combinations that would be necessary to drive the car.
import RPi.GPIO as GPIO
import time
Forward = 3
Backward = 5
Left = 7
Right = 8

chan_list = [Forward, Backward, Left, Right]

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(chan_list, GPIO.OUT)
	GPIO.output(chan_list, GPIO.LOW)

def destroy():
	GPIO.output(chan_list, GPIO.LOW)
	GPIO.cleanup()

def go(Direction):
	GPIO.output(chan_list, GPIO.LOW)
	GPIO.output(Direction, GPIO.HIGH)

def test_routine():
	while True:

		go(Forward)
		time.sleep(1)

		go(Backward)
		time.sleep(1)

		go(Left)
		time.sleep(1)

		go(Right)
		time.sleep(1)

		go([Forward, Right])
		time.sleep(1)

		go([Forward, Left])
		time.sleep(1)

		go([Backward, Right])
		time.sleep(1)
	
		go([Backward, Left])
		time.sleep(1)

if __name__ == '__main__':
	setup()
	try:
		test_routine()

	except KeyboardInterrupt:
		destroy()
		
