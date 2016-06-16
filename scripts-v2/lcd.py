#!/usr/bin/python

# Python library for LTS01A MLAB module with MAX31725 i2c Local Temperature Sensor

#uncomment for debbug purposes
#import logging
#logging.basicConfig(level=logging.DEBUG) 

import time
import datetime
import sys
from pymlab import config

#### Sensor Configuration ###########################################

cfg = config.Config(
    i2c = {
        "port": 1, # for ODROID C1
    },

    bus = [
        {
            "type": "i2chub",
            "address": 0x70,
            
            "children": [
                {"name": "lcd", "type": "i2clcd", "address": 0x27, "channel": 5, }
            ],
        },
    ],
)


cfg.initialize()

lcd = cfg.get_device("lcd")
lcd.route()
lcd.reset()
lcd.init()
n = 0

#### Data Logging ###################################################

try:
    while 1:    
        sys.stdout.write("Cvak\n")
        sys.stdout.flush()
        lcd.init()
        lcd.light(1)
        time.sleep(0.5)
        lcd.light(0)

        lcd.puts('Cvak.')

        time.sleep(0.5)
        lcd.set_row2()

        lcd.light(1)
        time.sleep(0.5)
        lcd.light(0)

        sys.stdout.write("Hmmm\n")
        sys.stdout.flush()
        lcd.puts('Hmmm...')
        time.sleep(2)

except KeyboardInterrupt:
    sys.exit(0)
