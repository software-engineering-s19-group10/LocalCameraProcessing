from websocket_server import WebsocketServer
import base64, numpy, io, binascii
from PIL import Image
import wss, asyncio

import time
clients = None
FRAME_QUEUE = None


loop = asyncio.get_event_loop()

server = wss.Server(port=8080, usessl=True, sslcert="cert.pem",
                     sslkey="key.pem", auth=None)

def onTextMessage(msg, client):
	pass

def onBinaryMessage(msg, client):
	pass

@asyncio.coroutine
def incrementClientCount(client, server):
	global clients
	clients.value = clients.value + 1
	print("A client connected... There are now " + str(clients.value) + " clients.")
	if(clients.value <= 1):
		while(True):
			time.sleep(0.01)
			if(clients.value>0 and not(FRAME_QUEUE.empty())):
				frame = FRAME_QUEUE.get()
				if(not(frame is None)):
					frameBytes = io.BytesIO();
					Image.fromarray(frame).save(frameBytes,'jpeg')
					server.send_message_to_all(binascii.b2a_base64(frameBytes.getvalue()))
				else:
					continue


def decrementClientCount(client, server):
	global clients
	clients.value = clients.value - 1
	print("A client disconnected... There are now " + str(clients.value) + " clients.")


def startServer(q, streamerClients, portNum):
	global clients
	clients = streamerClients

	global FRAME_QUEUE

	FRAME_QUEUE = q

	server = wss.Server(port=portNum, usessl=True, sslcert="cert.pem",
                     sslkey="key.pem", auth=None)
	server.setTextHandler(onTextMessage)
	server.setBinaryHandler(onBinaryMessage)
	loop.create_task(incrementClientCount())
	# server.set_fn_client_left(decrementClientCount)
	print("Streaming server [ON]...")
	server.start()
	loop.run_forever()
	
