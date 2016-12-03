"""
com_config.py v 1.0.2
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import configparser
import os.path

config_file = "config/config.ini"


def setconfig():
    acquisitionduration = 3  # In hours
    config = configparser.ConfigParser()
    
    # region Config
    # Version
    config['APPLICATION'] = {}
    config['APPLICATION']['name'] = 'Time Lapse'
    config['APPLICATION']['version'] = '1.0.0'
    config['APPLICATION']['author'] = '© Bruno DELATTRE'
    
    # Acquisition
    config['ACQUISITION'] = {}
    config['ACQUISITION']['trigger'] = '5'
    
    # LOGGER
    config['LOGGER'] = {}
    config['LOGGER']['levelconsole'] = '10'  # DEBUG=10 INFO=20 WARNING=30 ERROR=40 #CRITICAL=50
    config['LOGGER']['levelfile'] = '20'
    config['LOGGER']['logfile'] = 'log'
    config['LOGGER']['logfilesize'] = '1000000'
    
    # Export
    config['EXPORT'] = {}
    config['EXPORT']['directoryimage'] = 'pictures'
    
    # SQLite
    config['SQLITE'] = {}
    config['SQLITE']['database'] = 'database.db'
    
    # Camera v8M 3280x2464 -- v5M 2592x1944
    config['CAMERA'] = {}
    config['CAMERA']['pic_resolution_x'] = '2592'
    config['CAMERA']['pic_resolution_y'] = '1944'
    config['CAMERA']['vid_resolution_x'] = '1920'
    config['CAMERA']['vid_resolution_y'] = '1080'
    config['CAMERA']['framerate'] = '30'
    config['CAMERA']['rotation'] = '0'
    config['CAMERA']['brightness'] = '0'
    config['CAMERA']['contrast'] = '0'
    # negative, solarise, posterize, whiteboard, blackboard, sketch, denoise, emboss, oilpaint, hatch, gpen, pastel, watercolour, film, blur, saturation
    config['CAMERA']['image_effect'] = ''
    # auto, night, nightpreview, backlight, spotlight, sports, snow, beach, verylong, fixedfps, antishake, fireworks
    config['CAMERA']['exposure_mode'] = 'auto'
    # average, spot, backlit, matrix
    config['CAMERA']['meter_mode'] = 'average'
    # off, auto, sun, cloud, shade, tungsten, fluorescent, incandescent, flash, horizon
    config['CAMERA']['awb'] = 'auto'
    config['CAMERA']['picture_path'] = 'pictures/'
    config['CAMERA']['delay'] = '3'
    config['CAMERA']['nb'] = str(int(((acquisitionduration * 3600) / float(config['CAMERA']['delay']))))
    
    # GPIO
    config['GPIO'] = {}
    
    # LED
    config['GPIO']['LED_ACQUISITION'] = '23'
    
    # INPUT
    config['GPIO']['INPUT_ACQUISITION'] = '27'
    # endregion
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, config_file)
    with open(db_path, 'w') as configfile:
        config.write(configfile)


def getconfig():
    config = configparser.RawConfigParser()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, config_file)
    config.read(db_path)
    return config
