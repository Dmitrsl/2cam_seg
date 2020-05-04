
import datetime
import threading
import time

import cv2
import os
import numpy as np
from flask import Flask, Response, render_template
from flask_bootstrap import Bootstrap

from harvesters.core import Harvester
import traceback
import sys

app = Flask(__name__)

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        generate(self.previewName)

def generate(previewName):
    """Video streaming generator function."""
    if previewName == 'harvesters':

        h = Harvester()
        h.add_cti_file('/opt/mvIMPACT_Acquire/lib/x86_64/mvGenTLProducer.cti')
        h.update_device_info_list()
        ia = h.create_image_acquirer(0)
        ia.remote_device.node_map.ExposureTimeRaw.value = 20_000
        #ia.dremote_deviceevice.node_map.PixelFormat.value = 'BayerRG8'
        #ia.remote_device.node_map.TestPattern = 'HorizontalColorBar' 
        time.sleep(1)   
        try:
            ia.start_image_acquisition()
            i = 0
            done = False

            while not done:
                with ia.fetch_buffer() as buffer:
                    img = buffer.payload.components[0].data
                    img = img.reshape(buffer.payload.components[0].height, buffer.payload.components[0].width)
                    img_copy = img.copy()
                    img_copy = cv2.cvtColor(img, cv2.COLOR_BayerRG2RGB)

                    if i == 0:
                        first = img_copy.copy()

                    is_change = np.allclose(first, img_copy, 3)    
                    #print(is_change)
                    if not is_change:
                        
                        # cv2.namedWindow("window", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
                        # cv2.imshow("window", img_copy)
                        # cv2.imwrite(f'./images/image_{i}.png', img_copy)
                        img_copy_ = cv2.resize(img_copy, (640, 480))

                        frame = cv2.imencode('.jpg', img_copy_)[1].tobytes()
                        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                    first = img_copy.copy()

                    if cv2.waitKey(10) == ord('q'):
                        fps = ia.statistics.fps
                        print("FPS: ", fps)
                        done = True
                        print('break')
                    i = i + 1
                    # if i == 200:
                    #     break
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
        finally:
            ia.stop_image_acquisition()
            ia.destroy()
            print('fin')
            h.reset()

    else:

        cap = cv2.VideoCapture(0)

        # Read until video is completed
        while(cap.isOpened()):
        # Capture frame-by-frame
            ret, img = cap.read()
            if ret == True:
                img = cv2.resize(img, (0, 0), fx=1, fy=1)
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                time.sleep(0.001)
            else:
                break


@app.route("/")
def index():

    return render_template('index.html', title='Online')


@app.route("/video_feed_harvesters")
def video_feed_harvesters():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate('harvesters'),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/video_feed")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate('webcamera'),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

# Create two threads as follows
thread1 = camThread("harvesters", 1)
thread2 = camThread("webcamera", 2)
thread1.start()
thread2.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)