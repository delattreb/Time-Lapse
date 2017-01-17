"""
main.py v 1.1.5
Auteur: Bruno DELATTRE
Date : 03/12/2016
"""

from acquisition import thread_acquisition_camera_timer
from lib import com_config, com_gpio_inout, com_logger

# Config
conf = com_config.Config()
conf.setconfig()
config = conf.getconfig()

# Log
logger = com_logger.Logger('TIMELAPSE')
logger.info(config['APPLICATION']['name'] + ' ' + config['APPLICATION']['version'] + ' ' + 'Start')

# Init
gpioinout = com_gpio_inout.GPIOINOT()
delayqcquition = 0
tabdelay = [2, 4, 6, 8, 10]
timedelay = 3
gpioinout.blink(0.2, 3)

# Waiting for Init acquisition
logger.info('Wait for start')
logger.info('Delay: ' + str(tabdelay[delayqcquition] + timedelay))
while not gpioinout.getstart():
    # Check config
    if gpioinout.getconfigacquisition():
        delayqcquition += 1
        if delayqcquition >= len(tabdelay):
            delayqcquition = 0
        gpioinout.blink(0.15, delayqcquition + 1)
        logger.debug('Delay: ' + str(tabdelay[delayqcquition] + timedelay))

logger.warning('Start acquition - Delay: ' + str(tabdelay[delayqcquition] + timedelay))
gpioinout.blink(0.8, 3)

camera_thread = thread_acquisition_camera_timer.ThreadAcquisitionCameraTimer(tabdelay[delayqcquition])
camera_thread.start()
