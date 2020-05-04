import cv2
import harvesters
from harvesters.core import Harvester
import numpy as np  # This is just for a demonstration.

from harvesters.core import Harvester
import sys
import traceback
import cv2

def main():
    h = Harvester()
    h.add_cti_file('/opt/mvIMPACT_Acquire/lib/x86_64/mvGenTLProducer.cti')
    h.update_device_info_list()
    ia = h.create_image_acquirer(0)
    ia.remote_device.node_map.PixelFormat.value = 'BayerRG8'
    #ia.device.node_map.TestPattern = 'HorizontalColorBar'
    ia.remote_device.node_map.ExposureTimeRaw.value = 10000
    #print(dir(ia.remote_device.node_map))
    print(h.device_info_list[0])  
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
                cv2.namedWindow("window", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
                cv2.imshow("window", img_copy)
                print(img_copy.shape)
                fps = ia.statistics.fps
                print("FPS: ", fps)
                if cv2.waitKey(10) == ord('q'):
                    done = True
                    print('break')
                i = i + 1
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    finally:
        ia.stop_image_acquisition()
        ia.destroy()
        cv2.destroyAllWindows()
        print('fin')
        h.reset()

if __name__ == "__main__":
    main()