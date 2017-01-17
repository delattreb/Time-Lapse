"""
thread_acquisition_camera.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import sqlite3
from threading import Timer

from lib import com_camera, com_config, com_gpio_inout


class ThreadAcquisitionCameraTimer:
    def __init__(self, lock, delay):
        super().__init__()
        self.delay = delay
        self.lock = lock
        self.hFunction = self.getpicture
        self.thread = Timer(self.delay, self.handle_function)
        
        conf = com_config.Config()
        config = conf.getconfig()
        self.database = config['SQLITE']['database']
        self.instance = com_camera.Camera('PICTURE')
        
        # GPIO
        self.gpioinout = com_gpio_inout.GPIOINOT()
    
    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.delay, self.handle_function)
        self.thread.start()
    
    def start(self):
        self.thread.start()
    
    def cancel(self):
        self.thread.cancel()
    
    def getpicture(self):
        self.lock.acquire()
        
        connection = sqlite3.Connection(self.database)
        cursor = connection.cursor()
        self.instance.getpicture(connection, cursor)
        
        self.lock.release()
        
        # Blink at each picture taken
        self.gpioinout.blink(0.04, 1)
