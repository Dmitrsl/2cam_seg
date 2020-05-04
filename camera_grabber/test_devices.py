from harvesters.core import Harvester

import numpy as np  # This is just for a demonstration.

h = Harvester()

h.add_cti_file('/opt/mvIMPACT_Acquire/lib/x86_64/mvGenTLProducer.cti')

h.update_device_info_list()

print(h.device_info_list[0])