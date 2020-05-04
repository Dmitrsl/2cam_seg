from harvesters.core import Harvester
import numpy as np
import sys
import traceback
import cv2

def main():
    h = Harvester()
    h.add_cti_file('/opt/mvIMPACT_Acquire/lib/x86_64/mvGenTLProducer.cti')
    h.update_device_info_list()
    ia = h.create_image_acquirer(0)
    #ia.device.node_map.PixelFormat.value = 'BayerRG8'
    #ia.device.node_map.TestPattern = 'HorizontalColorBar'    
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
                print(is_change)
                if not is_change:
                    
                    # cv2.namedWindow("window", cv2.WINDOW_KEEPRATIO | cv2.WINDOW_NORMAL)
                    # cv2.imshow("window", img_copy)
                    cv2.imwrite(f'./images/image_{i}.png', img_copy)
                first = img_copy.copy()

                if cv2.waitKey(10) == ord('q'):
                    fps = ia.statistics.fps
                    print("FPS: ", fps)
                    done = True
                    print('break')
                i = i + 1
                if i == 200:
                    break
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