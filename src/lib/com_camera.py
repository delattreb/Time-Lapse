"""
com_camera.py v1.0.1
Auteur: Bruno DELATTRE
Date : 15/09/2016
"""

# Source https://www.raspberrypi.org/learning/getting-started-with-picamera/worksheet/

try:
    from picamera import PiCamera
except Exception as exp:
    PiCamera = None

from time import sleep

from dal import dal_camera, dal_picture
from lib import com_config, com_logger


def is_plugged(function):
    def plugged(*original_args, **original_kwargs):
        return function(*original_args, **original_kwargs)
    
    if not PiCamera:
        logger = com_logger.Logger('CAMERA')
        logger.warning('Camera not plugged')
    
    return plugged


class Camera:
    @is_plugged
    def __init__(self, mode):
        if PiCamera is not None:
            self.imgName = 'PIC_'
            self.vidName = 'VID_'

            conf = com_config.Config()
            config = conf.getconfig()
            logger = com_logger.Logger('CAMERA')
            
            self.camera = PiCamera()
            if mode == 'PICTURE':
                self.camera.resolution = (int(config['CAMERA']['pic_resolution_x']), int(config['CAMERA']['pic_resolution_y']))
                logger.debug('Init Camera mode PICTURE: ' + config['CAMERA']['pic_resolution_x'] + ' ' + config['CAMERA']['pic_resolution_y'])
            if mode == 'VIDEO':
                self.camera.resolution = (int(config['CAMERA']['vid_resolution_x']), int(config['CAMERA']['vid_resolution_y']))
                logger.debug('Init Camera mode VIDEO: ' + config['CAMERA']['vid_resolution_x'] + ' ' + config['CAMERA']['vid_resolution_y'])
                self.camera.framerate = int(config['CAMERA']['framerate'])
            
            # self.camera.brightness = config['CAMERA']['brightness']
            # self.camera.contrast = config['CAMERA']['contrast']
            # self.camera.image_effect = config['CAMERA']['image_effect']
            # self.camera.exposure_mode = config['CAMERA']['exposure_mode']
            
            self.camera.rotation = config['CAMERA']['rotation']
            self.camera.meter_mode = config['CAMERA']['meter_mode']
            self.camera.awb_mode = config['CAMERA']['awb']
            self.path = config['CAMERA']['picture_path']
            self.camera.iso = 100
    
    def getpicture(self, connection, cursor):
        if PiCamera is not None:
            dalcamera = dal_camera.DALCamera(connection, cursor)
            dalpicture = dal_picture.DALPicture(connection, cursor)
            
            index = dalcamera.get_last_picture_id()
            name = self.path + self.imgName + str(index) + '.jpg'
            self.camera.capture(name)
            
            dalcamera.set_last_picture_id(index + 1)
            dalpicture.setpicture(name)
            
            logger = com_logger.Logger('CAMERA')
            logger.info('Picture taken:' + name)
    
    def getvideo(self, duration, connection, cursor):
        if PiCamera is not None:
            dal = dal_camera.DALCamera(connection, cursor)
            dalpicture = dal_picture.DALPicture(connection, cursor)
            
            index = dal.get_last_video_id()
            name = self.path + self.vidName + str(index) + '.h264'
            self.camera.start_recording(name)
            sleep(duration)
            self.camera.stop_recording()
            
            dal.set_last_video_id(index + 1)
            dalpicture.setvideo(name)
            
            logger = com_logger.Logger('CAMERA')
            logger.debug('Video taken: ' + name)
