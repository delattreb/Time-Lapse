"""
lcd.py v1.0.0
Auteur: Bruno DELATTRE
Date : 13/11/2016
"""

import time

from lib import com_config, com_logger, com_ssd1306


class LCD:
    def __init__(self):
        conf = com_config.Config()
        self.config = conf.getconfig()
        self.lcd = com_ssd1306.SSD1306()
    
    def displayoff(self):
        self.lcd.offscreen()
    
    def splash(self):
        self.lcd.clear()
        self.lcd.rectangle(0, 0, self.lcd.width_max - 1, self.lcd.height_max - 1)
        self.lcd.text(4, 1, self.config['APPLICATION']['name'], 2)
        self.lcd.text(4, 17, self.config['APPLICATION']['version'], 1)
        self.lcd.text(4, 49, self.config['APPLICATION']['author'], 0)
        
        self.lcd.display()
        time.sleep(int(self.config['APPLICATION']['splashduration']))

    def wait(self):
        self.lcd.clear()
        self.lcd.text(1, 25, 'Wait...', 2)
        self.lcd.display()
    
    def displaystartacquisition(self):
        logger = com_logger.Logger()
        cpt = int(self.config['ACQUISITION']['trigger'])
        for i in range(cpt):
            self.lcd.clear()
            self.lcd.text(36, 5, '- START -', 1)
            self.lcd.text(55, 35, str(int(self.config['ACQUISITION']['trigger']) - i), 3)
            self.lcd.display()
            time.sleep(1)
            logger.debug('Start in: ' + str(int(self.config['ACQUISITION']['trigger']) - i))
