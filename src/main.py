"""
main.py v 1.1.5
Auteur: Bruno DELATTRE
Date : 03/12/2016
"""

import threading

from acquisition import thread_acquisition_camera
from lib import com_config, com_gpio_inout, com_logger

# Config
conf = com_config.Config()
conf.setconfig()
config = conf.getconfig()

# Log
logger = com_logger.Logger('TIMELAPSE')
logger.info(config['APPLICATION']['name'] + '' + config['APPLICATION']['version'] + ' ' + 'start')

# Init
gpioinout = com_gpio_inout.GPIOINOT()
delayqcquition = 0
tabdelay = [5, 10, 15, 20, 25]
gpioinout.blink(0.3, 3)

# Waiting for Init acquisition
logger.info('Wait for start')
logger.info('Delay: ' + str(tabdelay[delayqcquition]))
while not gpioinout.getstart():
    # Check config
    if gpioinout.getconfigacquisition():
        delayqcquition += 1
        if delayqcquition >= len(tabdelay):
            delayqcquition = 0
        gpioinout.blink(0.2, delayqcquition + 1)
        logger.debug('Delay: ' + str(tabdelay[delayqcquition]))

logger.info('Start acquition - Delay: ' + str(tabdelay[delayqcquition]))
gpioinout.blink(0.8, 3)

threadlock = threading.Lock()
camera_thread = thread_acquisition_camera.ThreadAcquisitionCamera("Camera Thread", threadlock, tabdelay[delayqcquition])
camera_thread.start()
camera_thread.join()
gpioinout.blink(0.3, 3)
logger.info('Application stop')
