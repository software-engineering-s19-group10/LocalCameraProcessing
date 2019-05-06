import time
import math
import requests
import base64, numpy, io, binascii
from PIL import Image
import lockCtrl
from cv2 import COLOR_BGR2RGB, COLOR_BGR2GRAY, CascadeClassifier, cvtColor, CASCADE_SCALE_IMAGE

#Constants
THRESHOLD_FULL = 5 #MAX THRESHOLD CONSTANT

CURRENT_NAME = None
BOX = None
THRESHOLD = THRESHOLD_FULL
STARTINGTIME = None
FRAME = None

def sendDetectionQR():
    print("Sending QR...")
    r = requests.post('https://boiling-reef-89836.herokuapp.com/lock_owners/api/events/', json={"event_type": "Unlocked by QR code.", "duration":0, "lock":lockCtrl.lockid()})
    rstatus = r.status_code

def sendDetection(frame, box, name, duration, postURL):
	print("Recognized " + name + ". Duration: " + str(duration))
	r = None
	if(name == "Unknown"):
		frameRGB = Image.fromarray(cvtColor(frame, COLOR_BGR2RGB)).crop(box)
		frameBytes = io.BytesIO()
		frameRGB.save(frameBytes,'jpeg')
		r = requests.post(postURL,json={"event_type":"Stranger ", "duration":duration, "lock":lockCtrl.lockid(), "filename":str(time.time()),"image_bytes":binascii.b2a_base64(frameBytes.getvalue())})
		r_local = requests.post("http://245d3089.ngrok.io/lock_owners/api/events/?lock=1&event_type=Stranger&duration=0&filename=" + str(time.time()) + "&image_bytes=" + base64.b64encode(frameBytes.getvalue()).decode('utf-8'))
	else:
		r = requests.post(postURL,json={"event_type":"Unlocked by " + name, "duration":duration, "lock":lockCtrl.lockid()})

def eventLogger(frame, box, name, postURL):
	global CURRENT_NAME
	global BOX
	global THRESHOLD
	global STARTINGTIME
	global FRAME
	if(box != None):
		BOX = box
		FRAME = frame
	if((CURRENT_NAME != name) and (CURRENT_NAME != None)):
		THRESHOLD = THRESHOLD - 1
	else:
		THRESHOLD = THRESHOLD_FULL
		if(CURRENT_NAME != name):
			STARTINGTIME = time.time()
		CURRENT_NAME = name

	if(THRESHOLD == 0):
		duration = int(math.floor(time.time() - STARTINGTIME))
		sendDetection(FRAME, BOX, CURRENT_NAME, duration, postURL)
		if(name != None):
			CURRENT_NAME = name
			BOX = box
			STARTINGTIME = time.time()
			FRAME = frame
		else:
			CURRENT_NAME = None
			STARTINGTIME = None
			BOX = None
			FRAME = None
		THRESHOLD = THRESHOLD_FULL
