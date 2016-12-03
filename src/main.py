"""
main.py v 1.1.5
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import threading

import lcd
from acquisition import thread_acquisition_camera
from lib import com_config, com_gpio_inout, com_logger

# TODO try catch on all thread acquisition

# Config
com_config.setconfig()
config = com_config.getconfig()

# Log
logger = com_logger.Logger()
logger.info('Application start')

# LCD
lcd = lcd.LCD()

# LCD Splash
lcd.splash()

gpioinout = com_gpio_inout.GPIOINOT()
# Waiting for Init acquisition
"""
while not gpioinout.getacquisition():
    logger.info('Wait for input acquisition')
    lcd.displatSensor()
"""
gpioinout.blink(0.2, 5)

logger.info('Wait for trigger')
lcd.displaystartacquisition()
lcd.displayoff()
logger.info('Start acquition')

# Create new threads
threadlock = threading.Lock()

camera_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera Thread", threadlock, float(config['CAMERA']['delay']), int(config['CAMERA']['nb']))

camera_thread.start()

# Wait end for each thread
camera_thread.join()

logger.info('Application stop')
gpio = com_gpio_inout.GPIOINOT()
gpio.cleanup()
