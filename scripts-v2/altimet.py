#!/usr/bin/python

# Python test script for MLAB ALTIMET01A sensor

import time
import datetime
import sys
#import logging 
#logging.basicConfig(level=logging.DEBUG) 


from pymlab import config

#### Sensor Configuration ###########################################
try:
    cfg = config.Config(
        i2c = {
            "port": 1, # for ODROID C1
        },

        bus = [
            {
                "type": "i2chub",
                "address": 0x70,
                
                "children": [
                    {"name": "altimet", "type": "altimet01" , "channel": 4, },   
                ],
            },
        ],
    )

except IndexError:
    sys.stdout.write("Invalid configuration number.")
    sys.exit(1)

cfg.initialize()
gauge = cfg.get_device("altimet")
time.sleep(0.5)

#### Data Logging ###################################################

sys.stdout.write("ALTIMET data acquisition system started \n")

try:
    with open("ALTIMET_log.csv", "a") as f:
        while True:
            gauge.route()
            (t1, p1) = gauge.get_tp()
            sys.stdout.write(" Temperature: %.2f  Pressure: %d \n" % (t1, p1))
            sys.stdout.flush()
            time.sleep(0.5)
            f.write("%d,%.3f,%d\n" % (time.time(), t1, p1))
except KeyboardInterrupt:
    sys.stdout.write("\r\n")
    sys.exit(0)
    f.close()

