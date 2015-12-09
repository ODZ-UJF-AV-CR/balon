#!/usr/bin/python

# Retrieve CPU temperature

import sys
import logging
import time

def get_cputemp():
  # CPU Temperature
   logging.debug("Retrieving: CPU thermal sensor data")
   try: 
     with open("/sys/class/thermal/thermal_zone0/temp") as cputempf:
       cputemp=cputempf.readline()
       cputempf.close()
       cputemp=float(cputemp.rstrip())/1000.0
       logging.debug('CPU Temperature %.2f C' % cputemp)
       sensors['CPU_Temp'] = cputemp
       return(True)
   except IOError:
     logging.critical('CPU Temperature sensor not available.')
     return(False)

#### main ####
if __name__ == '__main__':
  logging.info('Starting CPU temperature readout')
  while True:
    if get_cputemp():
      print "CPU Temp: %.2f" % sensors['CPU_Temp']
    time.sleep(2)
