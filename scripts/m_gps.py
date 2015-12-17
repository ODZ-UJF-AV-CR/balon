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

import random

gpsd = None #seting the global variable

# Dictionaries for last read and last valid data
data = {}
lv_data = {}

NaN = float('nan')
def isnan(x): return str(x) == 'nan'

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
    avg_cr = None      # Moving average climb rate
    avg_over = 30.0    # Average over last half minute
    data['GPS_AvgClimb'] = NaN
    while self.running:
      #logging.debug("Retrieving GPS data.")
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
      data['GPS_Time']=gpsd.utc
      if (len(data['GPS_Time']) == 0):
        data['GPS_Time'] = NaN
      data['GPS_Fix']=gpsd.fix.mode
      data['GPS_Alt']=gpsd.fix.altitude
      data['GPS_Lat']=gpsd.fix.latitude
      data['GPS_Lon']=gpsd.fix.longitude
      data['GPS_Speed']=gpsd.fix.speed
      data['GPS_Track']=gpsd.fix.track
      data['GPS_Climb']=gpsd.fix.climb
      # Fake data for climb calc test
      #data['GPS_Climb']=0.01*random.randint(400,600)
      data['GPS_epx']=gpsd.fix.epx # Position error [m]
      data['GPS_epv']=gpsd.fix.epv # Altitude error [m]
      data['GPS_eps']=gpsd.fix.eps # Speed error [m/s]

      if (data['GPS_Fix'] > 2):
        if (avg_cr == None):
          avg_cr = data['GPS_Climb']
        avg_cr = (avg_cr*(avg_over - 1.0) + data['GPS_Climb'])/avg_over
        data['GPS_AvgClimb'] = avg_cr  
        for k in data.keys():
          lv_data[k] = data[k]  
      #logging.info(self.get_status_string())
      #logging.debug(self.get_lv_status_string())

  def get_status_string(self):
    status_string = "GPSTime: %s Fix: %d Alt: %f (%f) m Track: %f Climb: %f AvgClimb: %f Speed: %f (%f) m/s Lat: %f Lon: %f (%f m)" % (dv('GPS_Time'), dv('GPS_Fix'), dv('GPS_Alt'), dv('GPS_epv'), dv('GPS_Track'), dv('GPS_Climb'), dv('GPS_AvgClimb'), dv('GPS_Speed'), dv('GPS_eps'), dv('GPS_Lat'), dv('GPS_Lon'), dv('GPS_epx'))
    return(status_string)

  def get_lv_status_string(self):
    status_string = "LV GPSTime: %s Fix: %d Alt: %f (%f) m Track: %f Climb: %f Speed: %f (%f) m/s \nLat: %f Lon: %f (%f m)" % (lv('GPS_Time'), lv('GPS_Fix'), lv('GPS_Alt'), lv('GPS_epv'), lv('GPS_Track'), lv('GPS_Climb'), lv('GPS_Speed'), lv('GPS_AvgClimb'), lv('GPS_eps'), lv('GPS_Lat'), lv('GPS_Lon'), lv('GPS_epx'))
    return(status_string)

  def get_record(self):
    return(str("%s\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t" % (str(dv('GPS_Time')), dv('GPS_Fix'), dv('GPS_Alt'), dv('GPS_Speed'), dv('GPS_Track'), dv('GPS_Climb'), dv('GPS_AvgClimb'), dv('GPS_epx'), dv('GPS_epv'), dv('GPS_eps'), dv('GPS_Lat'), dv('GPS_Lon'))))

  def get_header(self):
    return('GPS_date_UTC\tGPS_fix\tGPS_alt\tGPS_speed\tGPS_track\tGPS_climb\tGPS_avgClimb\tGPS_epx\tGPS_epv\tGPS_eps\tLatitude\tLongitude\t')

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
    print "%-24s %3s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s %-10s" % ('UTC','Fix','Alt','Speed','Track','Climb','AvgClimb', 'PosErr','AltErr','SpeedErr','Latitude','Longitude')
    while gpsp.running:
      time.sleep(1)
      print "%24s %3d %10f %10f %10f %10f %10f %10f %10f %10f %10f %10f" % (str(dv('GPS_Time')), dv('GPS_Fix'), dv('GPS_Alt'), dv('GPS_Speed'), dv('GPS_Track'), dv('GPS_Climb'), dv('GPS_AvgClimb'), dv('GPS_epx'), dv('GPS_epv'), dv('GPS_eps'), dv('GPS_Lat'), dv('GPS_Lon'))
      #print gpsp.get_record()
  except (KeyboardInterrupt, SystemExit):
    logging.error("Exiting:")
    if gpsp.running:
      gpsp.running = False
      logging.info("GPS thread asked to shut down.")
    sys.exit(0)
