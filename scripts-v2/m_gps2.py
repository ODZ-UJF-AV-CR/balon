#!/usr/bin/python

# Monitor script GPS part, communicates with gpsd and acquires time

import time
import datetime
import sys
import logging 
import re

import m_settings as g
import os
from gps import *
import time

# Get sensor value or -1 if not available
def dv(sname):
  if sname in g.data:
    return(g.data[sname])
  else:
    return(-1)

NaN = float('nan')

# GPS get header
def get_alt():
  return(dv('GPS_Alt'))
 
def get_fix():
  return(dv('GPS_Fix'))

def get_status_string():
  status_string = "GPSTime: %s Fix: %d Alt: %f (%f) m Track: %f Speed: %f (%f) m/s Lat: %f Lon: %f (%f m)" % (dv('GPS_Time'), dv('GPS_Fix'), dv('GPS_Alt'), dv('GPS_epv'), dv('GPS_Track'), dv('GPS_Speed'), dv('GPS_eps'), dv('GPS_Lat'), dv('GPS_Lon'), dv('GPS_epx'))
  return(status_string)

def get_record():
  return(str("%s\t%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t" % (str(dv('GPS_Time')), dv('GPS_Fix'), dv('GPS_Alt'), dv('GPS_Speed'), dv('GPS_Track'),  dv('GPS_epx'), dv('GPS_epv'), dv('GPS_eps'), dv('GPS_Lat'), dv('GPS_Lon'))))

def get_header():
  return('GPS_date_UTC\tGPS_fix\tGPS_alt\tGPS_speed\tGPS_track\tGPS_climb\tGPS_epx\tGPS_epv\tGPS_eps\tLatitude\tLongitude\t')

def process_next():
  while gpsd.waiting()
    logging.info('Retrieving data from gpsd buffer')
    gpsd.next() 
  
    time_re = re.compile('^(.+)T(.+)Z$')

    while self.running:
      #logging.debug("Retrieving GPS data.")
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
      g.data['Epoch'] = time.time()
      g.data['GPS_DateTime']=gpsd.utc
      if (len(g.data['GPS_DateTime']) == 0):
        g.data['GPS_DateTime'] = NaN
        g.data['GPS_Date'] = NaN
        g.data['GPS_Time'] = NaN
      else:
        tre = time_re.match(data['GPS_DateTime'])
        if tre:
          g.data['GPS_Date'] = tre.group(1)
          g.data['GPS_Time'] = tre.group(2)
        else:
          logging.warn('Can not parse: ' + str(g.data['GPS_DateTime']))

      data['GPS_Fix']=gpsd.fix.mode
      data['GPS_Alt']=gpsd.fix.altitude
      data['GPS_Lat']=gpsd.fix.latitude
      data['GPS_Lon']=gpsd.fix.longitude
      data['GPS_Speed']=0.514444*gpsd.fix.speed
      data['GPS_Track']=gpsd.fix.track
      data['GPS_epx']=gpsd.fix.epx # Position error [m]
      data['GPS_epv']=gpsd.fix.epv # Altitude error [m]
      data['GPS_eps']=gpsd.fix.eps # Speed error [m/s]

#### main ####
if __name__ == '__main__':
  # Logging
  logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
    )
  try:
    gpsd = gps(mode=WATCH_ENABLE)
    while True:
      process_next()
      logging.info(get_status_string())
      time.sleep(1)
  except (KeyboardInterrupt, SystemExit):
    logging.error("Exiting:")
