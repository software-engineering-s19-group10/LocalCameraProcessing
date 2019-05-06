from pyzbar import pyzbar
import cv2, time
import requests
import lockCtrl
import eventLogger
postURL = None

def start(q, postURLe):
	global postURL
	postURL = postURLe
	print("QR Service [ON]...")
	while True:
		time.sleep(0.01)
		if(not(q.empty())):
			frame = q.get()
			QRs = pyzbar.decode(frame)
			for QR in QRs:
				postCode(QR)


def postCode(QR):
	barcodeData = QR.data.decode("utf-8")
	print("[INFO] Found QR: {}".format(barcodeData))
	r = requests.get(postURL+barcodeData)
	resultStatus = r.status_code
	if(r.json().get("status") == 200):
		print("QR authorized!")
		eventLogger.sendDetectionQR()
		lockCtrl.unlock()
	else:
		print("QR unauthorized!")
