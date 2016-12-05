"""
com_gpio_inout.py v1.0.2
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import time

from lib import com_config, com_gpio, com_logger


class GPIOINOT:
    def __init__(self):
        self.gpio = com_gpio.GPIODialog('LED ACQUISITION')
        self.gpio.setmodebcm()

        conf = com_config.Config()
        self.config = conf.getconfig()
        
        # LED ACQUISITION
        self.led_acquisition = int(self.config['GPIO']['LED_ACQUISITION'])
        self.gpio.setup(self.led_acquisition, self.gpio.OUT)

        # START ACQUISITION
        self.start_acquisition = int(self.config['GPIO']['START_ACQUISITION'])
        self.gpio.setuppud(self.start_acquisition, self.gpio.IN, self.gpio.PUD_DOWN)

        # STOP ACQUISITION
        self.stop_acquisition = int(self.config['GPIO']['STOP_ACQUISITION'])
        self.gpio.setuppud(self.stop_acquisition, self.gpio.IN, self.gpio.PUD_DOWN)
    
    def setacquisition(self, state):
        self.gpio.setio(self.led_acquisition, state)
        
        logger = com_logger.Logger('LED_ACQUISITION')
        logger.debug('LED: ' + str(state))

    def getstart(self):
        state = self.gpio.getio(self.start_acquisition)
        
        if state:
            logger = com_logger.Logger('START_ACQUISITION')
            logger.debug('INPUT START')
    
        return state

    def getstop(self):
        state = self.gpio.getio(self.stop_acquisition)
    
        if state:
            logger = com_logger.Logger('STOP_ACQUISITION')
            logger.debug('INPUT STOP')
        
        return state
    
    def blink(self, duration, repetition):
        blink_duration = duration
        cpt = 0
        while cpt < repetition:
            self.setacquisition(True)
            time.sleep(blink_duration)
            self.setacquisition(False)
            time.sleep(blink_duration)
            cpt += 1
    
    def cleanup(self):
        self.gpio.cleanup()
