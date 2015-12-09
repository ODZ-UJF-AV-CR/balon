#!/usr/bin/python

# Monitor script GPS part
# Adapted from code by Dan Mandle http://dan.mandle.me September 2012, License: GPL 2.0 

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

gpsd = None #seting the global variable

# Logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                    )

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

# GPS thread initialization and startup
gpsp = GpsPoller() # create the thread
gpsp.start() # start it up

# Get sensor value or -1 if not available
def sv(sname):
  if sname in sensors:
    return(sensors[sname])
  else:
    return(-1)

def get_gpsdata():
  # GPS data 
  logging.debug("Retrieving: GPS data")
            
  sensors['GPS_Time']=gpsd.utc
  sensors['GPS_Fix']=gpsd.fix.mode
  sensors['GPS_Alt']=gpsd.fix.altitude
  sensors['GPS_Lat']=gpsd.fix.latitude
  sensors['GPS_Lon']=gpsd.fix.longitude
  sensors['GPS_Speed']=gpsd.fix.speed
  sensors['GPS_Climb']=gpsd.fix.climb 

#### main ####
if __name__ == '__main__':
  try:
    while gpsp.running and get_gpsdata():
      print Running 
  except (KeyboardInterrupt, SystemExit):
    logging.error("Exiting:")
    if gpsp.running:
      gpsp.running = False
      logging.info("GPS thread asked to shut down.")
    sys.exit(0)

