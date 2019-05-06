import RPi.GPIO as GPIO
import time
from lock import lock180
from lock import unlock0

LOCK_ID = None
unlockTimeout = 0

def set_lockid(lockID):
	global LOCK_ID
	LOCK_ID = lockID
	
def lockid():
	global LOCK_ID
	return LOCK_ID

def unlock():
	global unlockTimeout
	curTime = time.time()
	if((curTime - unlockTimeout) > 15):
		print("Unlocking!")
		unlock0()
		time.sleep(5)
		lock180()	
		time.sleep(1)
		GPIO.cleanup()
		unlockTimeout = time.time()
