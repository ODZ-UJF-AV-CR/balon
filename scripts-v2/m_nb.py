#!/usr/bin/python
#
# Threaded NB poller
# 

import time
import datetime
import threading
import logging
import serial
import math

#### NB poller ####
class NB_poller(threading.Thread):
  # Default data dir
  data_dir = '/data/balon/'
  def __init__(self):
      logging.info("NB poller thread is initializing.")
      threading.Thread.__init__(self)
      self.running = True
      self.name = 'NB'

  def run(self):
    global sensors
    logging.info("NB thread is starting.")
    try:
      ser = serial.Serial('/dev/ttyUSB0',timeout=5)
      logging.info("Port opened for NB readout: %s" % (ser.name))
      # Reset the buffer and set start time
      ser.write(b'x')
      restime = time.time()
    except IOError as e:
      logging.critical('Failed to open for NB readout: %s' % e)
      self.running = False

    try:
      ttsleep = 5 # Number of seconds to sleep
      datafname = self.data_dir+"data_nb.csv"
      logging.info('NB data will be appended to: %s' % (datafname))
      with open(datafname, "a") as nbf:
        while self.running:
          # Sleep for a moment
          #logging.info('Sleeping for: %i seconds.' % ( ttsleep ))
          time.sleep(ttsleep)
          # Readout
          ser.write(b'r')
          record = ser.readline().lstrip().rstrip()
          looptime = time.time()-restime
          oldrestime = restime;

          ser.write(b'x')
          restime = time.time()

          records = record.split(',')  
          logging.info("{} events recorded in {:.2f} since {:s}.".format(records[0], looptime, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(oldrestime))))

          if ((float(records[0]) > 900) and (ttsleep > 1)) :
             ttsleep = math.floor(0.8*ttsleep); 
             logging.warn("Risk of NB overflow decreasing NB readout delay to %f.", ttsleep)
          
          nbf.write(str(oldrestime) + "," + str(looptime) + "," + str(record) + "\n")
          nbf.flush()
          
          message = 'not set'

    except IOError as e:
      logging.critical("%s" % e)
      self.running = False

    ser.close()
    nbf.close()

    logging.info("NB poller thread exiting.")
    self.running = False
# end of NB_poller

#### main ####
if __name__ == '__main__':
  try:
    logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                      )

    logging.info('Starting NB readout')
    nb = NB_poller()
    nb.start()
    while nb.isAlive():
      time.sleep(2)
  except (KeyboardInterrupt,SystemExit):
    nb.running = False
    logging.info("NB thread asked to exit")
 
  nb.join()

