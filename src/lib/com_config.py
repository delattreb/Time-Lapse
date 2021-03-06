"""
com_config.py v 1.0.2
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import configparser
import os.path

config_file = "config/config.ini"


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()

    def setconfig(self):
        # region Config
        # Version
        self.config['APPLICATION'] = {}
        self.config['APPLICATION']['name'] = 'Time-Lapse'
        self.config['APPLICATION']['version'] = '1.3.1'
        self.config['APPLICATION']['author'] = 'c Bruno DELATTRE'
        self.config['APPLICATION']['splashduration'] = '5'

        # Acquisition
        self.config['ACQUISITION'] = {}
        self.config['ACQUISITION']['trigger'] = '5'
        
        # LOGGER
        self.config['LOGGER'] = {}
        self.config['LOGGER']['levelconsole'] = '20'  # DEBUG=10 INFO=20 WARNING=30 ERROR=40 #CRITICAL=50
        self.config['LOGGER']['levelfile'] = '20'
        self.config['LOGGER']['logfile'] = 'log'
        self.config['LOGGER']['logfilesize'] = '1000000'

        # Camera v8M 3280x2464 -- v5M 2592x1944
        self.config['CAMERA'] = {}
        self.config['CAMERA']['ISO'] = '100'  # 100 - 800
        self.config['CAMERA']['pic_resolution_x'] = '2592'
        self.config['CAMERA']['pic_resolution_y'] = '1944'
        self.config['CAMERA']['vid_resolution_x'] = '1920'
        self.config['CAMERA']['vid_resolution_y'] = '1080'
        self.config['CAMERA']['framerate'] = '30'
        self.config['CAMERA']['rotation'] = '180'  # 0 - 359
        self.config['CAMERA']['brightness'] = '50'  # 0 - 100
        self.config['CAMERA']['contrast'] = '0'  # -100 - 100
        self.config['CAMERA']['raw'] = ''  # yuv rgb rgba bgr bgra
        self.config['CAMERA']['jpegquality'] = '100'
        self.config['CAMERA']['image_effect'] = ''  # negative, solarise, posterize, whiteboard, blackboard, sketch, denoise, emboss, oilpaint, hatch, gpen, pastel, watercolour, film, blur, saturation
        self.config['CAMERA']['exposure_mode'] = 'auto'  # auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks
        self.config['CAMERA']['meter_mode'] = 'average'  # average, spot, backlit, matrix
        self.config['CAMERA']['awb'] = 'auto'  # off, auto, sun, cloud, shade, tungsten, fluorescent, incandescent, flash, horizon
        self.config['CAMERA']['picture_path'] = 'pictures/'
        
        # GPIO
        self.config['GPIO'] = {}
        # LED
        self.config['GPIO']['LED_ACQUISITION'] = '17'
        # INPUT
        self.config['GPIO']['CONFIG_ACQUISITION'] = '27'
        self.config['GPIO']['START_ACQUISITION'] = '22'
        # endregion

        # Export
        self.config['EXPORT'] = {}
        self.config['EXPORT']['directoryimage'] = 'pictures'

        # SQLite
        self.config['SQLITE'] = {}
        self.config['SQLITE']['database'] = 'database.db'
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, config_file)
        with open(db_path, 'w') as configfile:
            self.config.write(configfile)
    
    def getconfig(self):
        self.config = configparser.RawConfigParser()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, config_file)
        self.config.read(db_path)
        return self.config
