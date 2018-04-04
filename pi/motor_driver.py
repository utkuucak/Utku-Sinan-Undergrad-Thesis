"""Helpers for controlling the Front and Back Motors"""
import RPi.GPIO as GPIO

class Motors():
    
    def __init_(self):
        print('Motors Class OK')
    def set_right_mode(self):
        """Set mode to Right"""
        GPIO.output(19, True)
        GPIO.output(26, False)

    def set_left_mode(self):
        """Set mode to Left"""
        GPIO.output(19, False)
        GPIO.output(26, True)

    def set_reverse_mode(self):
        """Set mode to Reverse"""
        GPIO.output(17, False)
        GPIO.output(27, True)

    def set_forward_mode(self):
        """Set mode to Forward"""
        GPIO.output(17, True)
        GPIO.output(27, False)

    def set_idle_mode(self):
        """Set mode to Idle"""
        self.set_back_motor_to_idle()
        self.set_front_motor_to_idle()

    def set_back_motor_to_idle(self):
        """Sets the Back motor to Idle state"""
        GPIO.output(17, True)
        GPIO.output(27, True)

    def set_front_motor_to_idle(self):
        """Sets the Front motor to Idle state"""
        GPIO.output(19, True)
        GPIO.output(26, True)

    def set_gpio_pins(self):
        """Sets the GPIO pins for the two motors"""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(27, GPIO.OUT)
        GPIO.setup(19, GPIO.OUT)
        GPIO.setup(26, GPIO.OUT)
        GPIO.setup(22, GPIO.OUT)

    def get_pwm_imstance(self):
        """Returns a PWM instance"""
        return GPIO.PWM(22, 100)

    def start_pwm(self,pwm):
        """Starts the PWM with the initial duty cycle"""
        pwm.start(100)

    def change_pwm_duty_cycle(self,pwm, duty_cycle):
        """Change the PWM duty cycle"""
        pwm.ChangeDutyCycle(duty_cycle)