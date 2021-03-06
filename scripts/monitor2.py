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

import m_settings as g
import m_pcrd
import m_gps
import m_gsm
import m_webcam
import m_cpu
import m_i2c

###################################################################
# Parts
pcrd_enabled    = False
webcam_enabled  = False
gsm_enabled     = False
gps_enabled     = False
cputemp_enabled = True
i2c_enabled     = True

#### Settings (webcam is separate) #####
#data_dir="/data/balon/"
log_dir=g.data_dir

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
  pcrd.data_dir = g.data_dir
  pcrd.start()
else:
  logging.warning("PCRD data capture disabled.")

###################################################################
# Webcam handler
if webcam_enabled:
  logging.info('Starting webcam handler')
  webcam = m_webcam.WebCamCapture()
  m_webcam.imagedir=g.image_dir
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

#### Data Logging ###################################################
logging.info("# Data acquisition system started")
runstart=time.time()

try:
    with open(g.data_dir+"data_log.csv", "a") as f:
        write_header=True
      
        while True:
            round_start=time.time()

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

            # i2c sensors
            if i2c_enabled:
	      i2c=m_i2c.get_i2c_data()
	      csv_header += i2c['header']
	      lr += i2c['record'] 

            # End of sensors, write out data
            lr=lr + "\n"
            logging.info("-------------- Writing to file ------------------------")
            if write_header:
              f.write('%s\n' % csv_header)
              write_header = False
            f.write(lr) 
	    f.flush()
            round_timeleft = g.round_beat + round_start - time.time()
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

