# from .cam import lastest_Cam
# from .cam import lastest_Cam2 
# from .realsense2 import rs2_AsyncCam
from .utils import *

version='0.0.5'

def getVersion():
    return version

def getCameraClass(type='rs2'):
    if type=='rs2':
        from .realsense2 import rs2_AsyncCam 
        return rs2_AsyncCam
    elif type=='cv':
        from .cam import lastest_Cam2
        return lastest_Cam2
    else:
        return None
