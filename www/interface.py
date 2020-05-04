import argparse
import datetime
import threading
import time

import cv2
import os
import imutils
import numpy as np
from flask import Flask, Response, render_template
from flask_bootstrap import Bootstrap

#from generate import generate
from stream import camera_stream
from harvesters.core import Harvester

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)
app.config.from_json('config.json')


@app.route("/")
def index():

    return render_template('index.html', title='Online')


@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

def generate():
	# grab global references to the output frame and lock variables
	global outputFrame, lock
	# loop over frames from the output stream
	while True:
		# wait until the lock is acquired
		with lock:
			# check if the output frame is available, otherwise skip
			# the iteration of the loop
			if outputFrame is None:
				continue
			# encode the frame in JPEG format
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			# ensure the frame was successfully encoded
			if not flag:
				continue
		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

# def generate():
# 	files = os.listdir('images/')
# 	for file in files:

# 		image = cv2.imread(f'images/{file}')
# 		(flag, encodedImage) = cv2.imencode(".jpg", image)
# 		#time.sleep(.1)
# 		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
# 				bytearray(encodedImage) + b'\r\n')


def server_run():
	app.run()

if __name__ == '__main__':
	#stream_thread = threading.Thread(target=camera_stream)

	#t.daemon = True
	print("* Starting camera service...")
	#stream_thread.start()
	# start the web server
	print("* Starting web service...")
	app.run()
	#camera_stream()
	#stream()
	
