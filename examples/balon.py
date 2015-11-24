#!/usr/bin/python

# Python test script for MLAB ALTIMET01A sensor

import time
import datetime
import sys
#import logging 
#logging.basicConfig(level=logging.DEBUG) 


from pymlab import config


#### Script Arguments ###############################################

'''
if len(sys.argv) not in (2, 3):
    sys.stderr.write("Invalid number of arguments.\n")
    sys.stderr.write("Usage: %s #I2CPORT\n" % (sys.argv[0], ))
    sys.exit(1)

port       = eval(sys.argv[1])
if len(sys.argv) > 2:
    cfg_number = eval(sys.argv[2])
else:
    cfg_number = 0
'''

cfg_number = 0
port = 4

#### Sensor Configuration ###########################################

cfglist=[
    config.Config(
        i2c = {
            "port": port,
        },

        bus = [
            {
                "type": "i2chub",
                "address": 0x73,
                
                "children": [
                    {"name": "altimet", "type": "altimet01" , "channel": 0, },   
        	    	{"name": "sht25", "type": "sht25", "channel": 5, },
                    {"name": "guage", "type": "lioncell", "channel": 3, },
                ],
            },
        ],
    ),
]

try:
    cfg = cfglist[cfg_number]
except IndexError:
    sys.stdout.write("Invalid configuration number.")
    sys.exit(1)

cfg.initialize()
altimet = cfg.get_device("altimet")
sht_sensor = cfg.get_device("sht25")
guage = cfg.get_device("guage")
time.sleep(0.5)

#### Data Logging ###################################################

sys.stdout.write("ALTIMET data acquisition system started \n")

try:
    with open("ALTIMET_log.csv", "a") as f:
        while True:
            altimet.route()
            (t1, p1) = altimet.get_tp()
            sys.stdout.write(" Temperature: %.2f  Pressure: %d " % (t1, p1))
            time.sleep(0.5)
            #f.write("%d,%.3f,%d\n" % (time.time(), t1, p1))
	
            sht_sensor.route()	    	
            temperature = sht_sensor.get_temp();
            humidity = sht_sensor.get_hum();
            sys.stdout.write(" Temperature: %.2f  Humidity: %.1f " % (temperature, humidity))
            #f.write("%d\t%s\t%.2f\t%.1f\t%d\n" % (time.time(), datetime.datetime.now().isoformat(), temperature, humidity, sht_sensor.setup(sht_config) ))


            guage.route()
            print "Temp =", guage.getTemp(), "degC, RemainCapacity =", guage.getRemainingCapacity(), "mAh, cap =", guage.FullChargeCapacity(), "mAh, U =", guage.Voltage(), "mV, I =", guage.AverageCurrent(), "mA, charge =", guage.StateOfCharge(), "%"


            sys.stdout.flush()

except KeyboardInterrupt:
    sys.stdout.write("\r\n")
    sys.exit(0)
    f.close()

