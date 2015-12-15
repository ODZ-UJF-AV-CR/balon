#!/usr/bin/python

# Monitor script

# GPS part from code by Dan Mandle http://dan.mandle.me September 2012, License: GPL 2.0 

import time
import datetime
import sys
import logging 
import re

import os
from gps import *
from time import *
import time
import threading

from pymlab import config

round_beat = 5 # Seconds for one round of data capture
data = {}

# Get sensor value or -1 if not available
def dv(sname):
  if sname in data:
    return(data[sname])
  else:
    return(-1)

class i2cSensors(threading.Thread):
  def __init__(self):
    logging.info("Starting Modem handler thread")
    threading.Thread.__init__(self)
    self.running = True


  #### Data Logging ###################################################
  def run(self):
    logging.info("# Data acquisition system started")
    
    #### Sensor Configuration ###########################################
    cfg_number = 0
    port = 4

    cfglist=[config.Config(i2c = {"port": port,},
    bus = [
        {
      "type": "i2chub",
      "address": 0x73,
      
      "children": [
        {"name": "altimet", "type": "altimet01" , "channel": 0, },   
        {"name": "sht25", "type": "sht25", "channel": 5, },
        {"name": "gauge", "type": "lioncell", "channel": 3, },
      ],
        },
    ],),]

    try:
      cfg = cfglist[cfg_number]
    except IndexError:
      logging.critical("Invalid configuration number.")
      sys.exit(1)

    # Initialize the hub
    logging.debug('Initializing I2C data')
    try:
      cfg.initialize()
    except IOError as e:
      logging.critical('Whole I2C bus unavailable: %s' % e)

    # Initialize 
    altimet = cfg.get_device("altimet")
    sht_sensor = cfg.get_device("sht25")
    gauge = cfg.get_device("gauge")
 
    time.sleep(0.5)

    while self.running:
      round_start=time.time()
      data['Epoch'] = round_start
      # System UTC epoch time
      csv_header = 'Epoch\t'
      lr="%d\t" % round_start
 
      # Altimet
      logging.debug("Retrieving: Altimet temperature and pressure data")
      try:
        altimet.route()
        (t1, p1) = altimet.get_tp()
        if (p1 == 0):
          logging.error('Altimet malfunction - no data from pressure indicator.')
        logging.info("AltiTemp: %.2f C Press: %d " % (t1, p1))
        data['Altimet_Temp'] = t1
        data['Altimet_Press'] = p1
      except IOError:
        logging.error('Altimet data unavailable %s' % e)

      csv_header = csv_header + 'T_Altimet\tPressure\t'
      lr=lr+("%.3f\t%d\t" % (dv('Altimet_Temp'), dv('Altimet_Press')))

      # SHT sensor  
      logging.debug("Retrieving: SHT sensor data")
      try:
        sht_sensor.route()        
        temperature = sht_sensor.get_temp()
        humidity = sht_sensor.get_hum()
        logging.info("SHTTemp: %.2f C Humid: %.1f " % (temperature, humidity))
        data['SHT_Temp'] = temperature
        data['SHT_Hum'] = humidity
      except IOError as e:
        logging.error('SHT data unavailable as %s' % e)

      csv_header = csv_header + 'T_SHT\tHumidity\t'
      lr=lr+("%.2f\t%.1f\t" % (dv('SHT_Temp'), dv('SHT_Hum')))

      # Battery data
      logging.debug("Retrieving: Battery sensor data")
      try:
        gauge.route()
        data['Bat_Temp'] = gauge.getTemp()
        data['Bat_RemCap'] = gauge.getRemainingCapacity()
        data['Bat_FullChargeCapacity'] = gauge.FullChargeCapacity()
        data['Bat_V'] = gauge.Voltage()
        data['Bat_AvgI'] = gauge.AverageCurrent()
        data['Bat_Charge'] = gauge.StateOfCharge()
        logging.info("BatTemp: %.2f C RemCap: %d mAh FullCap: %d mAh U: %d mV I: %d mA Charge: %.2f %%" % 
                        (data['Bat_Temp'], data['Bat_RemCap'], data['Bat_FullChargeCapacity'], data['Bat_V'], data['Bat_AvgI'], data['Bat_Charge']))
      except IOError as e:
        logging.error('Battery data unavailable: %s' % e)

      csv_header = csv_header + 'T_Bat\tRemCap_mAh\tCap_mAh\tU_mV\tI_mA\tCharge_pct'
      lr=lr + ("%.2f\t%d\t%d\t%d\t%d\t%.2f" % (dv('Bat_Temp'), dv('Bat_RemCap'), dv('Bat_FullChargeCapacity'), dv('Bat_V'), dv('Bat_AvgI'), dv('Bat_Charge')))

      print csv_header
      print lr
      tts = round_beat - (time.time()-round_start)
      if (tts > 0):
        time.sleep(tts)

#### main ####
if __name__ == '__main__':
  # Logging
  logging.basicConfig(level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
    )
  try:
    # GPS thread initialization and startup
    i2c = i2cSensors() # create the thread
    i2c.start() # start it up

  except (KeyboardInterrupt, SystemExit):
    logging.error("Exiting.")
    i2c.running = False
    sys.exit(0)

