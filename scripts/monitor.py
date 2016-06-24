#!/usr/bin/python

# Data acquisition control script
# Limited threading version

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
#import m_pcrd
import m_nb as nb
import m_gps
import m_cpu
import m_i2c

import m_reboot

# Get sensor value or -1 if not available
def dv(sname):
  if sname in g.data:
    return(g.data[sname])
  else:
    return(-1)

###################################################################
# Parts
nb_enabled      = True
pcrd_enabled    = False
gps_enabled     = True
cputemp_enabled = True
i2c_enabled     = True

#### Settings #####
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

# Start
logging.info("# Data acquisition script started")
run_start=time.time()

###################################################################
# NB
if nb_enabled:
  arr = ['Epoch','GPS_Alt[m]','Pressure[Pa]','Humidity1','Temp1','Humidity2','Temp2'] + nb.get_header()
  nb.store(arr)
  g.data['nb_restime'] = nb.nb_reset()

###################################################################
# GPS thread initialization and startup
if gps_enabled:
  logging.info("Initializing GPS interface.")
  try:
    g.data['GPS_AvgClimb'] = NaN
    g.data['GPS_Climb']=NaN

    gpsd = gps(mode=WATCH_ENABLE)
  except:
    logging.critical('GPS initialization failed: %s' % (e))
    gps_enabled = False
else:
  logging.warning("GPS interface disabled.")

#### Data Logging #################################################
logging.warn('This is boot nr {0}'.format(m_reboot.get_n_boot_times()))
logging.warn('Beat time is {0} s'.format(g.round_beat))
m_reboot.append_boot_time()

bootcount = m_reboot.get_n_boot_times()

try:
    with open(g.data_dir+"data_log.csv", "a") as f:
        write_header=True

        # Endless main loop 
        while True:
          try:
            round_start=time.time()
            g.data['Epoch'] = round_start
            lcdargs = []

            # System UTC epoch time
            csv_header = 'Epoch\t'
            lr="%d\t" % dv('Epoch')
 
            # GPS data 
            if gps_enabled:
              try:
                m_gps.process_next(gpsd) #this will continue to loop and grab EACH set of gpsd info to clear the buffer
                logging.info(m_gps.get_status_string())
                csv_header = csv_header + m_gps.get_header()
                lr = lr + m_gps.get_record()
              except:
                raise
              lcdargs.append('GPS %1.0f Alt %6.0f' % (dv('GPS_Fix'), dv('GPS_Alt')))
              lcdargs.append('p %5.0f a %6.0f' % (dv('Altimet_Press'), dv('Altimet_Alt')))

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
              m_i2c.lcd()

            # NB sensors
            if nb_enabled:
              # Gets an array, with sum of energies, number of pulses and then energies of events
              csv_header = csv_header + 'NB_looptime\tNB_Count\tNB_Sum\t'
              nb_records = nb.nb_retrieve()
              g.data['nb_restime'] = nb.nb_reset()

              nb_looptime = nb_records[0]
              nb_sum = nb_records[1]
              nb_count = nb_records[2]
            
              lr = lr + '\t'.join(map(str, [ '%.2f' % ( float(nb_looptime)), nb_count, nb_sum])) + '\t'

              lcdargs.append('NB %4.1f S %4.1f' % (float(nb_count/nb_looptime), float(nb_sum/nb_looptime)))
              if (nb_count > 999):
                lcdargs.append('>> NB OVERFLOW <<')

              nb.store([round_start, dv('GPS_Alt'), dv('Altimet_Press'), dv('SHT_Hum'), dv('SHT_Temp'), dv('SHT_Hum2'), dv('SHT_Temp2')] + nb_records)

            # If LCD available, update it
            if i2c_enabled:
              m_i2c.lcdargs(lcdargs)

          except ValueError as e:
           logging.critical("%s" % e)

          except TypeError as e:
            logging.critical("%s" % e)

          except IOError as e:
            logging.critical("%s" % e)
          
          finally:
            # End of sensors, write out data
            lr=lr + "\n"
            logging.info("-------------- Writing to file ------------------------\n")
            if write_header:
              f.write('%s\n' % csv_header)
              write_header = False
              
            f.write(lr) 
      	    f.flush()

            #################################################################  
            
            round_timeleft = g.round_beat + round_start - time.time()
            if (round_timeleft > 0) and (round_timeleft <= g.round_beat):
              time.sleep(round_timeleft)

except (KeyboardInterrupt, SystemExit):
    logging.error("Exiting.")
    #f.write("\r\n")
    f.close()
         
    sys.exit(0)

