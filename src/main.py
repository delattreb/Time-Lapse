"""
main.py v 1.1.5
Auteur: Bruno DELATTRE
Date : 03/12/2016
"""

import threading

import lcd
from acquisition import thread_acquisition_camera
from lib import com_config, com_gpio_inout, com_logger

# Config
conf = com_config.Config()
conf.setconfig()
config = conf.getconfig()

# Log
logger = com_logger.Logger()
logger.info('Application start')

# LCD
lcd = lcd.LCD()

# LCD Splash
lcd.splash()

# Wait...
lcd.wait()

# Waiting for Init acquisition
logger.info('Wait for start')
gpioinout = com_gpio_inout.GPIOINOT()
while not gpioinout.getstart():
    pass
logger.info('Wait for trigger')
lcd.displaystartacquisition()
lcd.displayoff()
logger.info('Start acquition')

threadlock = threading.Lock()
camera_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera Thread", threadlock, float(config['CAMERA']['delay']), int(config['CAMERA']['nb']))
camera_thread.start()
camera_thread.join()
