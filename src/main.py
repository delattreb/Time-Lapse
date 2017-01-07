"""
main.py v 1.1.5
Auteur: Bruno DELATTRE
Date : 03/12/2016
"""

import threading
from time import sleep

from acquisition import thread_acquisition_camera
from lib import com_config, com_gpio_inout, com_logger

# Config
conf = com_config.Config()
conf.setconfig()
config = conf.getconfig()

# Log
logger = com_logger.Logger()
logger.info(config['APPLICATION']['name'] + '' + config['APPLICATION']['version'] + ' ' + 'start')

# Init
gpioinout = com_gpio_inout.GPIOINOT()
delayqcquition = 0
tabdelay = [5, 10, 15, 20]
gpioinout.blink(0.1, tabdelay[delayqcquition])

# Waiting for Init acquisition
logger.info('Wait for start')
while not gpioinout.getstart():
    # Check config
    if gpioinout.getconfigacquisition():
        delayqcquition += 1
        if delayqcquition > len(tabdelay):
            delayqcquition = 0
        gpioinout.blink(0.1, tabdelay[delayqcquition])
    sleep(0.1)

logger.info('Start acquition')

threadlock = threading.Lock()
camera_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera Thread", threadlock, tabdelay[delayqcquition])
camera_thread.start()
camera_thread.join()

logger.info('Application stop')
