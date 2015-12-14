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

import m_pcrd
import m_gps
import m_gsm
import m_webcam
import m_cpu

###################################################################
# Parts
pcrd_enabled    = False
webcam_enabled  = True
gsm_enabled     = False
gps_enabled     = True
cputemp_enabled = True

#### Settings (webcam is separate) #####
data_dir="/data/balon/"
log_dir=data_dir
default_destination = "+420777642401"

round_beat = 5 # Seconds for one round of sensors capture

# Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                    filename=log_dir+'monitor.log'
                    )

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

#logging.basicConfig(level=logging.INFO,
#                    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
#                    )

###################################################################
# PCRD readout
if pcrd_enabled:
  logging.info('Starting PCRD readout')
  pcrd = m_pcrd.PCRD_poller()
  pcrd.data_dir = data_dir
  pcrd.start()
else:
  logging.warning("PCRD data capture disabled.")

###################################################################
# Webcam handler
if webcam_enabled:
  logging.info('Starting webcam handler')
  webcam = m_webcam.WebCamCapture()
  m_webcam.imagedir=data_dir+"img/"
  webcam.start()
else:
  logging.warning("Webcam image capture disabled.")

###################################################################
# GSM module 
if gsm_enabled:
  logging.info("Initializing GSM interface.")
  gsmpart = m_gsm.ModemHandler()
  gsmpart.start()
else:
  logging.warning("GSM interface disabled.")

###################################################################
# GPS thread initialization and startup
if gps_enabled:
  logging.info("Initializing GPS interface.")
  gpsp = m_gps.GpsPoller() # create the thread
  gpsp.start() # start it up
else:
  logging.warning("GPS interface disabled.")


#### Script Arguments ###############################################
cfg_number = 0
port = 4
sensors = {}

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
    logging.critical("Invalid configuration number.")
    sys.exit(1)

# Initialize the hub
logging.debug('Initializing I2C sensors')
try:
  cfg.initialize()
except IOError as e:
  logging.critical('Whole I2C bus unavailable: %s' % e)

# Initialize 
altimet = cfg.get_device("altimet")
sht_sensor = cfg.get_device("sht25")
guage = cfg.get_device("guage")

# Get sensor value or -1 if not available
def sv(sname):
  if sname in sensors:
    return(sensors[sname])
  else:
    return(-1)


#### Data Logging ###################################################

time.sleep(0.5)
logging.info("# Data acquisition system started")

#gpsp.join()

runstart=time.time()

try:
    with open(data_dir+"data_log.csv", "a") as f:
        write_header=True
      
        while True:
            round_start=time.time()
            sensors['Epoch'] = round_start
            # System UTC epoch time
            csv_header = 'Epoch\t'
            lr="%d\t" % round_start
 
            # GPS data 
            if gps_enabled:
              logging.info(gpsp.get_status_string())
              csv_header = csv_header + gpsp.get_header()
              lr = lr + gpsp.get_record()

            # GSM module data
            if gsm_enabled:
              logging.info(gsmpart.get_status_string())
              csv_header = csv_header + gsmpart.get_header()
              lr = lr + gsmpart.get_record()

            # CPU Temperature
            if cputemp_enabled:
              logging.info(m_cpu.get_status_string())
              csv_header = csv_header + m_cpu.get_header()
              lr=lr+m_cpu.get_record()

            # Altimet
            logging.debug("Retrieving: Altimet temperature and pressure data")
            try:
              altimet.route()
              (t1, p1) = altimet.get_tp()
              if (p1 == 0):
                logging.error('Altimet malfunction - no data from pressure indicator.')
              logging.info("AltiTemp: %.2f C Press: %d " % (t1, p1))
              sensors['Altimet_Temp'] = t1
              sensors['Altimet_Press'] = p1
            except IOError:
              logging.error('Altimet sensors unavailable %s' % e)

            csv_header = csv_header + 'T_Altimet\tPressure\t'
            lr=lr+("%.3f\t%d\t" % (sv('Altimet_Temp'), sv('Altimet_Press')))

            # SHT sensor	
            logging.debug("Retrieving: SHT sensor data")
            try:
              sht_sensor.route()	    	
              temperature = sht_sensor.get_temp()
              humidity = sht_sensor.get_hum()
              logging.info("SHTTemp: %.2f C Humid: %.1f " % (temperature, humidity))
              sensors['SHT_Temp'] = temperature
              sensors['SHT_Hum'] = humidity
            except IOError as e:
              logging.error('SHT sensors unavailable as %s' % e)

            csv_header = csv_header + 'T_SHT\tHumidity\t'
            lr=lr+("%.2f\t%.1f\t" % (sv('SHT_Temp'), sv('SHT_Hum')))

            # Battery sensors
            logging.debug("Retrieving: Battery sensor data")
            try:
              guage.route()
              sensors['Bat_Temp'] = guage.getTemp()
              sensors['Bat_RemCap'] = guage.getRemainingCapacity()
              sensors['Bat_FullChargeCapacity'] = guage.FullChargeCapacity()
              sensors['Bat_V'] = guage.Voltage()
              sensors['Bat_AvgI'] = guage.AverageCurrent()
              sensors['Bat_Charge'] = guage.StateOfCharge()
              logging.info("BatTemp: %.2f C RemCap: %d mAh FullCap: %d mAh U: %d mV I: %d mA Charge: %.2f %%" % 
                              (sensors['Bat_Temp'], sensors['Bat_RemCap'], sensors['Bat_FullChargeCapacity'], sensors['Bat_V'], sensors['Bat_AvgI'], sensors['Bat_Charge']))
            except IOError as e:
              logging.error('Battery sensors unavailable: %s' % e)

            csv_header = csv_header + 'T_Bat\tRemCap_mAh\tCap_mAh\tU_mV\tI_mA\tCharge_pct'
            lr=lr + ("%.2f\t%d\t%d\t%d\t%d\t%.2f" % (sv('Bat_Temp'), sv('Bat_RemCap'), sv('Bat_FullChargeCapacity'), sv('Bat_V'), sv('Bat_AvgI'), sv('Bat_Charge')))

            # End of sensors, write out data
            lr=lr + "\n"
            sensors['Ready']=True
            logging.info("Writing to file --------------------------------------------------------------------------------")
            if write_header:
	      #f.write("\nEpoch\tGPS_date_UTC\tGPS_fix\tGPS_alt\tGPS_speed\tGPS_climb\tLatitude\tLongitude\tGSM_signal\tGSM_CellInfo\tT_CPU\tT_Altimet\tPressure\tT_SHT\tHumidity\tT_Bat\tRemCap_mAh\tCap_mAh\tU_mV\tI_mA\tCharge_pct\n")
              f.write('%s\n' % csv_header)
              write_header = False
            f.write(lr) 
	    f.flush()
            round_timeleft = round_beat + round_start - time.time()
            if (round_timeleft > 0):
              time.sleep(round_timeleft)

except (KeyboardInterrupt, SystemExit):
    logging.error("Exiting:")
    #f.write("\r\n")
    f.close()
    if pcrd_enabled:
      try:
        pcrd.running = False
        logging.info("Requesting PCRD thread to shut down.")
      except NameError:
        logging.error("PCRD enabled, but not initialized?")     
    if gsm_enabled:
      try:
        gsmpart.running = False
        logging.info("Requesting GSM thread to shut down.")
      except NameError:
        logging.error("GSM part enabled, but not initialized?")     
    if webcam_enabled:
      try: 
        webcam.running = False
        logging.info("Requesting Webcam thread shut down.")
      except NameError:
        logging.error("Webcam part enabled, but not initialized?")
    if gps_enabled:
      try:
        gpsp.running = False
        logging.info("GPS thread asked to shut down.")
      except NameError:
        logging.error("GPS part enabled, but not initialized?")

    sys.exit(0)

