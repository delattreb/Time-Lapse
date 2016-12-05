"""
thread_acquisition_camera.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import sqlite3
import threading
import time

from lib import com_camera, com_config, com_gpio_inout, com_logger


class ThreadAcquisitionCamera(threading.Thread):
    def __init__(self, name, lock, delay, counter):
        super().__init__()
        conf = com_config.Config()
        config = conf.getconfig()
        self.name = name
        self.counter = counter
        self.delay = delay
        self.lock = lock
        self.database = config['SQLITE']['database']

        # GPIO
        self.gpioinout = com_gpio_inout.GPIOINOT()
    
    def run(self):
        logger = com_logger.Logger('Camera Thread')
        logger.info('Start')
        self.getpicture(self.delay, self.counter)
        logger.info('Stop')
    
    def getpicture(self, delay, counter):
        instance = com_camera.Camera('PICTURE')
        while counter and not self.gpioinout.getstop():
            self.lock.acquire()
            connection = sqlite3.Connection(self.database)
            cursor = connection.cursor()
            instance.getpicture(connection, cursor)
            self.lock.release()

            # Blink at each picture taken
            gpioinout = com_gpio_inout.GPIOINOT()
            gpioinout.blink(0.04, 1)
            
            counter -= 1
            time.sleep(delay)
