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
gsm_enabled     = True
gps_enabled     = True
cputemp_enabled = True
i2c_enabled     = True

low_power_mode = False


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
# GSM module 
if gsm_enabled:
  logging.info("Delaying initializing of GSM interface.")
  m_gsm.radio_on = False
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

###################################################################
# Webcam handler
if webcam_enabled:
  logging.info('Webcam handler startup delayed.')
else:
  logging.warning("Webcam image capture disabled.")


#### Data Logging ###################################################
logging.info("# Data acquisition system started")
run_start=time.time()
last_sos=time.time()

baloon_level='START'
test_alt = 220
test_cr = 0

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
              if m_gsm.radio_on:
                logging.info(gsmpart.get_status_string())
                lr = lr + gsmpart.get_record()
              csv_header = csv_header + m_gsm.get_header()

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
            logging.info("-------------- Writing to file ------------------------\n")
            if write_header:
              f.write('%s\n' % csv_header)
              write_header = False
              
            f.write(lr) 
      	    f.flush()

            ######################################################################
            # SWITCH LOW POWER MODE ON AND OFF

            # If voltage is low, set the low_power mode flag
            if i2c_enabled:
              if 'Bat_V' in i2c['data']:
                V = i2c['data']['Bat_V']
              else:
                V = None

              #logging.warn('Voltage: {0} {1}'.format(V, g.U_lpm))
              if (V < g.U_lpm[0]) and low_power_mode:
                # Switch to low power mode 
                logging.debug('Status: Low power mode ON')
              elif (V < g.U_lpm[0]) and not low_power_mode:
                # Switch to low power mode 
                logging.warn('Change: Low power mode ON')
                low_power_mode = True
              elif (V < g.U_lpm[1]) and low_power_mode:
                logging.debug('Status: Low power mode and not enough V to disable it.')
              elif not low_power_mode:
                logging.debug('Status: Low power mode OFF')
              else: 
                # Exit low power mode
                logging.warn('Change: Low power mode OFF')
                low_power_mode = False

            else:
              logging.info('i2c interface disabled, low power mode switching not available')
            #========================================================================

            # Start/stop the webcam using thresholds
            if webcam_enabled:
               if low_power_mode:
                 # Should be stopped
                 try:
                   if webcam.running and webcam.isAlive:
                     webcam.running = False
                     logging.warn('Change: Webcam running and alive, asked to stop.')
                   elif webcam.isAlive():
                     logging.warn('Webcam thread pending shutdown.')
                   else:
                     logging.info('Webcam thread is stopped.')
                 except NameError:
                   logging.info('OK: Webcam thread down due to low power mode.')
               else:
                 # Should be running
                 logging.debug('Webcam should be on. Checking.')
                 try:
                   if webcam.running and webcam.isAlive():
                     # Thread is alive and running 
                     logging.debug('OK: Webcam thread alive and running.')
                   elif webcam.isAlive() and not webcam.running:
                     logging.warn('ERR: Webcam is alive, but not marked as running.')
                   elif webcam.running and not webcam.isAlive():
                     logging.warn('ERR: Webcam marked as running, but thread is not alive.')
                   else:
                     logging.warn('Change: Restarting webcam')
                     webcam = m_webcam.WebCamCapture()
                     m_webcam.imagedir=g.image_dir
                     webcam.start()
                 except NameError as err:
                   logging.warn('Change: Enabling webcam thread as %s' % err)
                   webcam = m_webcam.WebCamCapture()
                   m_webcam.imagedir=g.image_dir
                   webcam.start()
            #endof webcam triggers
  
            if time.time() - run_start > 600 and time.time() - last_sos > 60:
              # If we are in air for so long, just try to connect
              m_gsm.radio_on = True
              if not 'position' in m_gsm.sms_queue:
                m_gsm.sms_queue.append('position')
                m_gsm.sms_queue.append('SOS')
              baloon_mode = 'FAILSAFE'
              last_sos = time.time()

            elif gsm_enabled and gps_enabled:
              # Height triggers for SMS and modem power
              # Get altitude - either from GPS or from barometric altimeter
              alt = NaN
              cr = NaN

              if 'GPS_Alt' in m_gps.data:
                alt = m_gps.data['GPS_Alt']
              elif i2c_enabled and 'Altimet_Alt' in m_i2c.data:
                alt = m_i2c.data['Altimet_Alt']
              else:
                alt = NaN
              
              if 'GPS_AvgClimb' in m_gps.data:
                cr = m_gps.data['GPS_AvgClimb']
              elif i2c_enabled and 'Altimet_Climb' in m_i2c.data:
                cr = m_i2c.data['Altimet_Climb'] 
              else:
                cr = NaN

              ### ---- TESTING
              if (test_alt > 350):
                test_cr = -1.5 * test_cr
              elif test_cr == 0 and time.time() - run_start > 60: 
                test_cr = 1.0

              cr = test_cr
              alt = test_alt + cr
              ### ____ TESTING
              
              if not math.isnan(alt) and not math.isnan(cr):
                #logging.warn('Altitude: {0} CR: {1}'.format(alt, cr))
                if cr > 0.5:
                  logging.warn(">>>> Ascending: {0} m {1} m/s".format(alt, cr))
                  if alt < 279:
                    # ODZ
                    logging.error("Radio on and reporting position, alt: {0}.".format(alt))
                    m_gsm.radio_on = True
                    if not 'position' in m_gsm.sms_queue and not baloon_level == 'A1':
                      m_gsm.sms_queue.append('position')
                    baloon_level='A1'
                  elif 279 <= alt < 300:
                    # Radio off, PCRD measuring
                    m_gsm.radio_on = False
                    baloon_level='A2'
                  elif 300 <= alt < 330:
                    # Send status
                    logging.error("Radio on and sending SMS messages: {0}.".format(alt))
                    m_gsm.radio_on = True
                    if not 'position' in m_gsm.sms_queue and not baloon_level == 'A3':
                      m_gsm.sms_queue.append('position')
                    baloon_level='A3'
                  elif 330 < alt:
                    # Radio off  
                    logging.error("Radio should be off: alt {0}.".format(alt))
                    m_gsm.radio_on = False
                    baloon_level='A4'
                  else:
                    logging.error("Ascending, but altitude makes no sense {0}.".format(alt))
                elif cr < -0.5:
                  logging.warn(">>>> Descending: {0} m {1} m/s".format(alt, cr))
                  # Just set modem to on and send position every minute
                  m_gsm.radio_on = True
                  if not 'position' in m_gsm.sms_queue and not baloon_level == 'D1':
                    m_gsm.sms_queue.append('position')
                  baloon_level = 'D1'
                else:
                  logging.warn(">>>> Stable altitude: {0} {1} m/s".format(alt, cr))
                  # Modem on
                  m_gsm.radio_on = True
                  if not 'position' in m_gsm.sms_queue and not baloon_level == 'GND':
                    m_gsm.sms_queue.append('position')
                  if baloon_level == 'D1':
                    m_gsm.sms_queue.append('The eagle has landed.')
                  baloon_level = 'GND'
              elif not math.isnan(alt):
                logging.warn('Altitude: {0} but no climb rate.'.format(alt))
              else:
                logging.warn('No altitude nor climb rate data.')

              logging.warn('Baloon mode: {0}, radio {1}.'.format(baloon_level, m_gsm.radio_on))
              if m_gsm.radio_on:
                try:
                  if gsmpart.running:
                    logging.info('Modem thread is alive. OK')
                  else:
                    logging.info('Modem thread exists, but not alive.')
                except:
                  #logging.info('Starting modem thread.')
                  gsmpart = m_gsm.ModemHandler()
                  gsmpart.start()
              else:
                try:
                  logging.info('Stopping modem thread.')
                  gsmpart.running = False
                except:
                  logging.info('Modem thread is stopped. OK.') 

              #logging.error(">>>>> GPS alt {0} cr {1} or {2} {3}".format(alt,cr,m_gps.dv('GPS_Alt'), m_gps.dv('GPS_Climb')))
              # end of height triggers

            round_timeleft = g.round_beat + round_start - time.time()
            if (round_timeleft > 0):
              time.sleep(round_timeleft)
              os.system('clear')

except (KeyboardInterrupt, SystemExit):
    logging.error("Exiting.")
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

