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
from random import randint
from time import sleep, time

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
            self.imgName = 'PIC' + str(randint(1000, 9000)) + '_'
            
            conf = com_config.Config()
            config = conf.getconfig()
            self.logger = com_logger.Logger('CAMERA')
            
            self.camera = PiCamera()
            if mode == 'PICTURE':
                self.camera.resolution = (int(config['CAMERA']['pic_resolution_x']), int(config['CAMERA']['pic_resolution_y']))
                self.logger.info('Camera mode PICTURE: ' + config['CAMERA']['pic_resolution_x'] + ' ' + config['CAMERA']['pic_resolution_y'])
            if mode == 'VIDEO':
                self.camera.resolution = (int(config['CAMERA']['vid_resolution_x']), int(config['CAMERA']['vid_resolution_y']))
                self.logger.debug('Init Camera mode VIDEO: ' + config['CAMERA']['vid_resolution_x'] + ' ' + config['CAMERA']['vid_resolution_y'])
                self.camera.framerate = int(config['CAMERA']['framerate'])
    
            self.camera.rotation = int(config['CAMERA']['rotation'])
            # self.camera.brightness = int(config['CAMERA']['brightness'])
            # self.camera.contrast = int(config['CAMERA']['contrast'])
            if len(config['CAMERA']['image_effect']) > 0:
                self.camera.image_effect = config['CAMERA']['image_effect']
            self.camera.exposure_mode = config['CAMERA']['exposure_mode']
            self.camera.meter_mode = config['CAMERA']['meter_mode']
            self.camera.awb_mode = config['CAMERA']['awb']
            if len(config['CAMERA']['raw']) > 0:
                self.camera.raw_format = config['CAMERA']['raw']
            self.path = config['CAMERA']['picture_path']
            self.camera.iso = int(config['CAMERA']['ISO'])
            self.quality = int(config['CAMERA']['jpegquality'])
            self.config = config
            self.index = 0
            self.last = time()
    
    def getpicture(self, connection, cursor):
        if PiCamera is not None:
            name = self.path + self.imgName + str(self.index) + '.jpg'
            
            self.camera.start_preview()
            sleep(2)
            if len(self.config['CAMERA']['raw']) > 0:
                self.camera.capture(name, 'raw')
            else:
                self.camera.capture(name, bayer = True, quality = self.quality)
            self.index += 1
            self.logger.info(name + ' ' + str(time() - self.last))
            self.last = time()
