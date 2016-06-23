#!/usr/bin/python

# Retrieve CPU temperature

import sys
import logging
import time

def get_header():
   return("T_CPU\t")

def get_status_string():
   return('CPU Temperature: %.2f C' % get_cputemp())

def get_record():
   return('%.2f\t' % get_cputemp())

def get_cputemp():
  # CPU Temperature
   logging.debug("Retrieving: CPU thermal sensor data")
   try: 
     with open("/sys/class/thermal/thermal_zone0/temp") as cputempf:
       cputemp=cputempf.readline()
       cputempf.close()
       cputemp=float(cputemp.rstrip())/1000.0
       return(cputemp)
   except IOError:
     logging.critical('CPU Temperature sensor not available.')
     return(-999.0)

#### main ####
if __name__ == '__main__':
  sensors = {}
  logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                      )

  logging.info('Starting CPU temperature readout')
  while True:
    logging.info(get_status_string())
    time.sleep(2)
