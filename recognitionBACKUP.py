from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import base64, numpy, io, binascii
import time
import requests
from PIL import Image
import eventLogger
import lockCtrl
from cv2 import COLOR_BGR2RGB, COLOR_BGR2GRAY, CascadeClassifier, cvtColor, CASCADE_SCALE_IMAGE
import cv2


embeddedDB = None
postURL = None
def fetchEmbedded():
	global embeddedDB
	#if(embeddedDB == None):
		#Force fetch DB
	#	r = requests.get(FORCE_ENDPOINT_HERE)
	#	embeddedDB = {"encodings": r.json().get("encodings"), "names": r.json().get("names")}
	#else:
	#	#Update DB if new images were added
	#	r = requests.get('https://boiling-reef-89836.herokuapp.com/lock_owners/api/recognition/get_embedded_data/')
	#	if(r.json().get("status") == 200):
	#		embeddedDB = {"encodings": r.json().get("encodings"), "names": r.json().get("names")}
	print("[INFO] Fetching embeddings...")
	embeddedDB = pickle.loads(open("encodings.pickle", "rb").read())
	



def start(q, postURLe):
	global embeddedDB
	global postURL
	postURL = postURLe
	embedUpdateTimeout = 0
	fetchEmbedded()
	detector = CascadeClassifier("haarcascade_frontalface_default.xml")
	while True:
		time.sleep(0.1)
		if(not(q.empty())):
			if(embedUpdateTimeout == 6):
				fetchEmbedded()
				embedUpdateTimeout = 0
			frame = imutils.resize(q.get(),width=500)
			frame = cvtColor(frame, COLOR_BGR2RGB)
			frameGray = cvtColor(frame, COLOR_BGR2GRAY)
			rects = detector.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),flags=CASCADE_SCALE_IMAGE)
			boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
			sendBoxes = [(x, y, x + w, y + h) for (x, y, w, h) in rects]
			encodings = face_recognition.face_encodings(frame, boxes)
			names = []
			
			for encoding in encodings:
				matches = face_recognition.compare_faces(embeddedDB["encodings"],encoding)
				name = "Unknown"
				if True in matches:
					matchedIdxs = [i for (i, b) in enumerate(matches) if b]
					counts = {}
					for i in matchedIdxs:
						name = embeddedDB["names"][i]
						counts[name] = counts.get(name, 0) + 1
					name = max(counts, key=counts.get)
				names.append(name)
			if(len(names) > 0):
				eventLogger.eventLogger(frame, sendBoxes[0], names[0],postURL)
				if(names[0] != "Unknown"):
					lockCtrl.unlock()
			else:
				eventLogger.eventLogger(frame, None, None,postURL)
			embedUpdateTimeout+=1
