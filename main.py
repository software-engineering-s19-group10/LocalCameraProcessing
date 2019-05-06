import multiprocessing
import time
import recognition
import qr
import streamer
from cv2 import cvtColor
from cv2 import COLOR_BGR2RGB
import imutils
import lockCtrl
from imutils.video import VideoStream

#CONSTANTS
LOCK_ID = 11 #LOCK NUMBER ASSOCIATED WITH THIS LOCK
STREAMING_PORT = 8080
CAPTURE_FRAMERATE = 1
API_ADDRESS = 'https://boiling-reef-89836.herokuapp.com'
QR_POST_URL = API_ADDRESS + '/lock_owners/api/temp_auth/verify/?auth_code='
EVENTS_POST_URL = API_ADDRESS + '/lock_owners/api/events/'

def unlock():
	print("Unlocking door...")


lockCtrl.set_lockid(LOCK_ID)
print("Starting processes...")
qStreamer = multiprocessing.Queue()
streamerClients = multiprocessing.Value('i',0)
pStreamer = multiprocessing.Process(target=streamer.startServer,args=[qStreamer,streamerClients,STREAMING_PORT,])
qQR = multiprocessing.Queue()
pQR = multiprocessing.Process(target=qr.start,args=[qQR,QR_POST_URL,])
qFR = multiprocessing.Queue()
pFR = multiprocessing.Process(target=recognition.start,args=[qFR,EVENTS_POST_URL,])
print("Starting camera...")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
print("Starting streaming service, QR service, and FR service...")
pStreamer.start()
pFR.start()
pQR.start()
while True:
	time.sleep((float)(1.0/CAPTURE_FRAMERATE))
	frameOriginal = vs.read()
	frame = imutils.resize(vs.read(), width=500)
	qQR.put(frameOriginal)
	qFR.put(frame)
	if(streamerClients.value > 0):
		streamRgb = cvtColor(frameOriginal, COLOR_BGR2RGB)
		qStreamer.put(streamRgb)
	
	
