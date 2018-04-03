import RPi.GPIO as GPIO
import time

LedPin = 8	# pin11

def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(LedPin, GPIO.OUT)
	GPIO.output(LedPin, GPIO.HIGH)

def blink():
	while True:
		GPIO.output(LedPin, GPIO.HIGH)	# led on
		time.sleep(0.5)
		GPIO.output(LedPin, GPIO.LOW)	# led off
		time.sleep(1)

def destroy():
	GPIO.output(LedPin, GPIO.LOW)	# led off
	GPIO.cleanup()			# release resource

if __name__ == '__main__':	# Program start from here
	
	setup()
	try:
		blink()
	except KeyboardInterrupt:	# When 'Ctrl+C' is pressed, the child program destroy() will be executed
		destroy()

