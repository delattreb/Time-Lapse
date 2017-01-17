"""
thread_acquisition_camera.py v1.0.0
Auteur: Bruno DELATTRE
Date : 17/09/2016
"""

import time
from threading import Timer


class ThreadTest:
    def __init__(self, delay):
        super().__init__()
        self.delay = delay
        self.hFunction = self.getpicture
        self.thread = Timer(self.delay, self.handle_function)
    
    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.delay, self.handle_function)
        self.thread.start()
    
    def start(self):
        self.thread.start()
    
    def cancel(self):
        self.thread.cancel()
    
    def getpicture(self):
        print(time.time())
