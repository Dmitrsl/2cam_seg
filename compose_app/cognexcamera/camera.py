from harvesters.core import Harvester
import traceback
import numpy as np
import time
import sys
import cv2
from flask import Flask, Response, render_template


app = Flask(__name__)


def generate():
    """Video streaming generator function."""
    h = Harvester()
    h.add_cti_file('/opt/mvIMPACT_Acquire/lib/x86_64/mvGenTLProducer.cti')
    h.update_device_info_list()
    ia = h.create_image_acquirer(0)
    #ia.device.node_map.PixelFormat.value = 'BayerRG8'
    #ia.device.node_map.TestPattern = 'HorizontalColorBar' 
    time.sleep(5)   
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
                    img_copy = cv2.resize(img_copy, (640, 480))
                    frame = cv2.imencode('.jpg', img_copy)[1].tobytes()
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


@app.route("/")
def index():
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)
