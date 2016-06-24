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
import m_nb
import m_gps 

# Mystic op
NaN = float('nan')
def isnan(x): return str(x) == 'nan'

avg_cr = None      # Moving average climb rate
g.data['Altimet_Climb'] = NaN

#### Sensor Configuration ###########################################
cfg_number = 0
port = 1

cfglist=[config.Config(i2c = {"port": port,},
bus = [
    {
  "type": "i2chub",
  "address": 0x70,
  
  "children": [
    {"name": "altimet", "type": "altimet01" , "channel": 4, },   
    {"name": "sht25", "type": "sht25", "channel": 7, },
    {"name": "sht25b", "type": "sht25", "channel": 1, },
    {"name": "gauge", "type": "lioncell", "channel": 3, },
    {"name": "lcd", "type": "i2clcd", "address": 0x27, "channel": 5, }
  ],
    },
],),]

try:
  cfg = cfglist[cfg_number]
except IndexError:
  logging.critical("Invalid configuration number.")
  sys.exit(1)

# Get sensor value or -1 if not available
def dv(sname):
  if sname in g.data:
    return(g.data[sname])
  else:
    return(-1)

#### Rough pressure to height conversion ###################################################
def press_to_height(pPa):
  # KPB dle ICAO
  t0 = 15.0 # C
  p0 = 1013.250 # hPa
  kC = 273.15
  
  if pPa > 1.0:
     p = pPa/100.0
     height = (kC + t0)/0.0065
     height = height * (1 - math.pow(p/p0,1.0/5.255))
     return(height)
  else:
    return(NaN) 

def lcdargs(lcdargs):
  try:
    cfg.initialize()
    lcd = cfg.get_device("lcd")

    lcd.route()
    lcd.reset()
    lcd.init()

    row=1
    logging.debug("LCD ARGS: " + ' '.join(lcdargs))
    for lcdarg in lcdargs:
      if row == 1:
	time.sleep(0.1)
	lcd.init()
	time.sleep(0.1)
	lcd.puts(lcdarg)
	row = 2
      else:
	time.sleep(0.1)
	lcd.set_row2()
	time.sleep(0.1)
	lcd.puts(lcdarg)
	time.sleep(1)
        row = 1
  except IOError as e:
    logging.error('LCD display not available: %s' % e)

def lcd():
  try:
    cfg.initialize()
    lcd = cfg.get_device("lcd")

    lcd.route()
    lcd.reset()
    lcd.init()

    time.sleep(0.1)
    time.sleep(0.1)

    lcd.puts('Bat %3.0f I %5.0f' % (dv('Bat_Charge'), -1*dv('Bat_AvgI')))
    lcd.set_row2()
    time.sleep(0.1)

    lcd.puts('H1 %4.1f H2 %4.1f' % (dv('SHT_Hum'), dv('SHT_Hum2')))
    #lcd.puts('H1 %4.1f H2 %4.1f' % (99.9, 99.9))
    time.sleep(0.9)
  except IOError as e:
    logging.error('LCD display not available: %s' % e)

#### i2c Data Logging ###################################################
def get_i2c_data():
  global status
  global avg_cr
  
  avg_over = 10.0    # Average over last ten measurements
  
  # Initialize the hub
  logging.debug('Initializing I2C bus')
  try:
    cfg.initialize()
  except IOError as e:
    logging.critical('Whole I2C bus unavailable: %s' % e)

  if 'Epoch' in g.data and 'Altimet_Alt' in g.data:
    #logging.info('Setting olds')
    g.data['Prev_Epoch'] = g.data['Epoch'] 
    g.data['Prev_Alt'] = g.data['Altimet_Alt'] 

  g.data['Epoch'] = time.time()

  # Initialize 
  altimet = cfg.get_device("altimet")
  sht_sensor = cfg.get_device("sht25")
  sht_sensor_2 = cfg.get_device("sht25b")
  gauge = cfg.get_device("gauge")

  time.sleep(0.5)

  csv_header = ''
  lr = ''

  # Altimet
  logging.debug("Retrieving: Altimet temperature and pressure data")
  try:
    altimet.route()
    (t1, p1) = altimet.get_tp()
    g.data['Altimet_Temp'] = t1
    g.data['Altimet_Press'] = p1
    g.data['Altimet_Alt'] = press_to_height(p1) 
    logging.info("AltiTemp: %.2f C  Press: %d Pa  Barometric height: %f m" % (t1, p1, g.data['Altimet_Alt']))

    # Calculate moving average ascent rate
    if (avg_cr == None) and not 'Prev_Alt' in g.data:
      g.data['Prev_Alt'] = g.data['Altimet_Alt']
    elif 'Prev_Alt' in g.data and 'Prev_Epoch' in g.data:
      climb = (g.data['Altimet_Alt'] - g.data['Prev_Alt'])/(g.data['Epoch'] - g.data['Prev_Epoch'])
      if (avg_cr == None):
        avg_cr = climb
      else:
        avg_cr = (avg_cr*(avg_over - 1.0) + climb)/avg_over
      g.data['Altimet_Climb'] = avg_cr
    logging.info('Barometric climb rate: {0} m/s'.format(avg_cr))
    
  except IOError as e:
    logging.error('Altimet data unavailable %s' % e)
    g.data.pop('Prev_Alt', None)

  csv_header = csv_header + 'T_Altimet\tPressure\tAlt_Alt\t'
  lr=lr+("%.3f\t%d\t%.1f\t" % (dv('Altimet_Temp'), dv('Altimet_Press'), dv('Altimet_Alt')))

  # SHT sensor  
  logging.debug("Retrieving: SHT sensor data")
  try:
    sht_sensor.route()        
    temperature = sht_sensor.get_temp()
    humidity = sht_sensor.get_hum()
    logging.info("SHTTemp: %.2f C Humid: %.1f " % (temperature, humidity))
    g.data['SHT_Temp'] = temperature
    g.data['SHT_Hum'] = humidity
  except IOError as e:
    logging.error('SHT data unavailable as %s' % e)

  csv_header = csv_header + 'T_SHT\tHumidity\t'
  lr=lr+("%.2f\t%.1f\t" % (dv('SHT_Temp'), dv('SHT_Hum')))
  
  # SHT sensor  
  logging.debug("Retrieving: SHT sensor data")
  try:
    sht_sensor_2.route()        
    temperature = sht_sensor_2.get_temp()
    humidity = sht_sensor_2.get_hum()
    logging.info("SHTTemp2: %.2f C Humid2: %.1f " % (temperature, humidity))
    g.data['SHT_Temp2'] = temperature
    g.data['SHT_Hum2'] = humidity
  except IOError as e:
    logging.error('SHT 2 data unavailable as %s' % e)

  csv_header = csv_header + 'T_SHT2\tHumidity2\t'
  lr=lr+("%.2f\t%.1f\t" % (dv('SHT_Temp2'), dv('SHT_Hum2')))

  # Battery data
  logging.debug("Retrieving: Battery sensor data")
  try:
    gauge.route()
    g.data['Bat_Temp'] = gauge.getTemp()
    g.data['Bat_RemCap'] = gauge.getRemainingCapacity()
    g.data['Bat_FullChargeCapacity'] = gauge.FullChargeCapacity()
    g.data['Bat_V'] = gauge.Voltage()
    g.data['Bat_AvgI'] = gauge.AverageCurrent()
    g.data['Bat_Charge'] = gauge.StateOfCharge()
    logging.info("BatTemp: %.2f C RemCap: %d mAh FullCap: %d mAh U: %d mV I: %d mA Charge: %.2f %%" % 
                    (g.data['Bat_Temp'], g.data['Bat_RemCap'], g.data['Bat_FullChargeCapacity'], g.data['Bat_V'], g.data['Bat_AvgI'], g.data['Bat_Charge']))
  except IOError as e:
    logging.error('Battery data unavailable: %s' % e)

  csv_header = csv_header + 'T_Bat\tRemCap_mAh\tCap_mAh\tU_mV\tI_mA\tCharge_pct\t'
  lr=lr + ("%.2f\t%d\t%d\t%d\t%d\t%.2f\t" % (dv('Bat_Temp'), dv('Bat_RemCap'), dv('Bat_FullChargeCapacity'), dv('Bat_V'), dv('Bat_AvgI'), dv('Bat_Charge')))

  status = {}
  status['header'] = csv_header
  status['record'] = lr
  status['data'] = dict(g.data)


  return(status)

#### main ####
if __name__ == '__main__':
  # Logging
  logging.basicConfig(level=logging.INFO,
    format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
    )

  while True:
    round_start=time.time()
    i2c=get_i2c_data()

    print "-----------------------------------------------------------------------"
    print i2c['header']
    print i2c['record']
    print "-----------------------------------------------------------------------"
   
    #print i2c['data']['Bat_V']
    
    tts = g.round_beat - (time.time()-round_start)
    if (tts > 0):
      time.sleep(tts)
    else:
      print "Beat too short"


