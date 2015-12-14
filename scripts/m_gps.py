#!/usr/bin/python

# Monitor script GPS part, communicates with gpsd and acquires time

import time
import datetime
import sys
import logging 
import re

import os
from gps import *
import time
import threading

gpsd = None #seting the global variable

# Dictionaries for last read and last valid data
data = {}
lv_data = {}

def dv(sname):
  if sname in data:
    return(data[sname])
  else:
    return(-1)

def lv(sname):
  if sname in lv_data:
    return(lv_data[sname])
  else:
    return(-1)

#### GPS Poller #####################################################
class GpsPoller(threading.Thread):
  global lv_data
  global data

  def __init__(self):
    logging.info("GPS poller thread initializing.")
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.running = True #setting the thread running to true

  def run(self):
    logging.info("GPS poller thread running.")
    global gpsd
    while self.running:
      #logging.debug("Retrieving GPS data.")
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
      data['GPS_Time']=gpsd.utc
      data['GPS_Fix']=gpsd.fix.mode
      data['GPS_Alt']=gpsd.fix.altitude
      data['GPS_Lat']=gpsd.fix.latitude
      data['GPS_Lon']=gpsd.fix.longitude
      data['GPS_Speed']=gpsd.fix.speed
      if (data['GPS_Fix'] > 2):
        for k in data.keys():
          lv_data[k] = data[k]  
      #logging.info(self.get_status_string())
      #logging.debug(self.get_lv_status_string())

  def get_status_string(self):
    status_string = "GPSTime: %s Fix: %d Alt: %.1f m Speed: %.1f m/s Lat: %f Lon: %f " % (dv('GPS_Time'), dv('GPS_Fix'), dv('GPS_Alt'), dv('GPS_Speed'), dv('GPS_Lat'), dv('GPS_Lon'))
    return(status_string)

  def get_lv_status_string(self):
    status_string = "LV GPSTime: %s Fix: %d Alt: %.1f m Speed: %.1f m/s Lat: %f Lon: %f " % (lv('GPS_Time'), lv('GPS_Fix'), lv('GPS_Alt'), lv('GPS_Speed'), lv('GPS_Lat'), lv('GPS_Lon'))
    return(status_string)

  def get_record(self):
    return(str("%s\t%d\t%.1f\t%.1f\t%.1f\t%f\t%f\t" % (str(dv('GPS_Time')), dv('GPS_Fix'), dv('GPS_Alt'), dv('GPS_Speed'), dv('GPS_Climb'), dv('GPS_Lat'), dv('GPS_Lon'))))

  def split_gps_time(gpstime, self):
    logging.info(lv('GPS_Time'))

#### main ####
if __name__ == '__main__':
  # Logging
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
    )
  try:
    # GPS thread initialization and startup
    gpsp = GpsPoller() # create the thread
    gpsp.start() # start it up
    while gpsp.running:
      time.sleep(1)
  except (KeyboardInterrupt, SystemExit):
    logging.error("Exiting:")
    if gpsp.running:
      gpsp.running = False
      logging.info("GPS thread asked to shut down.")
    sys.exit(0)
