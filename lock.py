#this is the lock-device function file
import time
import RPi.GPIO as GPIO

def lock180():
	#this function sets the servo to 180 degree (lock position)

	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT)

	p = GPIO.PWM(7,50)
	p.start(12.5)
	time.sleep(2.5)
	p.stop()
	GPIO.output(7,0)
	#GPIO.cleanup()


def unlock0():
	#this function sets the servo to 0 degree (unlock position)
	
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT)

	p = GPIO.PWM(7,50)
	p.start(2.5)
	time.sleep(2.5)
	p.stop()
	GPIO.output(7,0)
	#GPIO.cleanup()

