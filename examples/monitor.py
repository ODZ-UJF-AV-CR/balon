#!/usr/bin/python

# Monitor script

# GPS part from code by Dan Mandle http://dan.mandle.me September 2012, License: GPL 2.0 

import time
import datetime
import sys
import logging 

import os
from gps import *
from time import *
import time
import threading

logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
                    )
gpsd = None #seting the global variable

from pymlab import config

#### GPS Poller #####################################################
class GpsPoller(threading.Thread):
  def __init__(self):
    logging.info("Starting GPS poller thread")
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    logging.info("GPS poller thread running")
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

#### Script Arguments ###############################################

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

# GPS thread initialization
gpsp = GpsPoller() # create the thread
gpsp.start() # start it up
#### Data Logging ###################################################

sys.stdout.write("Data acquisition system started \n")

try:
    with open("data_log.csv", "a") as f:
	f.write("\nEpoch\tGPS_date_UTC\tGPS_fix\tGPS_alt\tLatitude\tLongitude\tT_CPU\tT_Altimet\tPressure\tT_SHT\tHumidity\tT_Bat\tRemCap_mAh\tCap_mAh\tU_mV\tI_mA\tCharge_pct\n")
        while True:
            # System UTC epoch time
            lr="%d\t" % time.time()
 
            # GPS data 
            logging.debug("Retrieving: GPS")
            zerotime=time.clock()
            while (gpsd.fix.mode < 2) and (time.clock() - zerotime < 10.0):
                  time.sleep(0.1) #set to whatever
            
            s=gpsd.utc
            gpsdatetime=s[:s.find('T')]+' '+s[s.find('T')+1:s.find('.')]
            sys.stdout.write("GPSTime: %s GPSfix: %d Alt: %.1f m Lat: %f Lon: %f " % (gpsdatetime, gpsd.fix.mode, gpsd.fix.altitude, gpsd.fix.latitude, gpsd.fix.longitude))
            lr = lr + ("%s\t%d\t%f\t%f\t%f\t" % (gpsd.utc, gpsd.fix.mode, gpsd.fix.altitude, gpsd.fix.latitude, gpsd.fix.longitude))

            # CPU Temperature
            logging.debug("Retrieving: CPU thermal sensor")
            with open("/sys/class/thermal/thermal_zone0/temp") as cputempf:
                cputemp=cputempf.readline()
                cputempf.close()
                cputemp=float(cputemp.rstrip())/1000.0
                sys.stdout.write("CPUTemp %.1f C " % cputemp)
                lr=lr+"%.2f\t" % (cputemp)

            # Altimet
            logging.debug("Retrieving: Altimet temperature and pressure")
            altimet.route()
            (t1, p1) = altimet.get_tp()
            sys.stdout.write("AltiTemp: %.2f C Press: %d " % (t1, p1))
            time.sleep(0.5)
            lr=lr+("%.3f\t%d\t" % (t1, p1))

            # SHT sensor	
            logging.debug("Retrieving: SHT sensor")
            sht_sensor.route()	    	
            temperature = sht_sensor.get_temp()
            humidity = sht_sensor.get_hum()
            sys.stdout.write("SHTTemp: %.2f C Humid: %.1f " % (temperature, humidity))
            lr=lr+("%.2f\t%.1f\t" % (temperature, humidity))

            # Battery sensors
            logging.debug("Retrieving: Battery sensors")
            guage.route()
            sys.stdout.write("BatTemp: %.2f C RemCap: %d mAh FullCap: %d mAh U: %d mV I: %d mA Charge: %.2f %%\n" % (guage.getTemp(), guage.getRemainingCapacity(), guage.FullChargeCapacity(), guage.Voltage(), guage.AverageCurrent(), guage.StateOfCharge()))
            #print "BatTemp: ", guage.getTemp(), "degC, RemainCapacity =", guage.getRemainingCapacity(), "mAh, cap =", guage.FullChargeCapacity(), "mAh, U =", guage.Voltage(), "mV, I =", guage.AverageCurrent(), "mA, charge =", guage.StateOfCharge(), "%"
            lr=lr + ("%.2f\t%d\t%d\t%d\t%d\t%.2f\n" % (guage.getTemp(), guage.getRemainingCapacity(), guage.FullChargeCapacity(), guage.Voltage(), guage.AverageCurrent(), guage.StateOfCharge()))
            logging.debug("Writing to file")
            f.write(lr) 
	    f.flush()
            sys.stdout.flush()

except (KeyboardInterrupt, SystemExit):
    sys.stdout.write("Exiting\r\n")
    #f.write("\r\n")
    f.close()
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    sys.exit(0)

print "Never get here."
gpsp.running = False
gpsp.join() # wait for the thread to finish what it's doing



