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

data = {}

# Get sensor value or -1 if not available
def dv(sname):
  if sname in data:
    return(data[sname])
  else:
    return(-1)

#### NB poller ####
class nb_poller(threading.Thread):
  global status
  global data

  # Default data dir
  data_dir = '/data/balon/'
  def __init__(self):
      logging.info("NB poller thread is initializing.")
      threading.Thread.__init__(self)
      self.running = True
      self.name = 'NB'

  def run(self):
  
    while self.running:
        global sensors
        logging.info("NB thread is starting.")
        try:
          ser = serial.Serial('/dev/ttyUSB0',timeout=5)
          logging.info("Port opened for NB readout: %s" % (ser.name))
          # Reset the buffer and set start time
          ser.write(b'x')
          restime = time.time()
        #except IOError as e:
        #  logging.critical('Failed to open for NB readout: %s' % e)
        #  self.running = False
        #  time.sleep(10)
        #except KeyboardInterrupt:
        #  ser.close()
        #  nbf.close()
        #  raise

        #try:
          ttsleep = 5 # Number of seconds to sleep
          datafname = self.data_dir+"data_nb.csv"
          logging.info('NB data will be appended to: %s' % (datafname))
          with open(datafname, "a") as nbf:
            while self.running:
              # Sleep for a moment
              #logging.info('Sleeping for: %i seconds.' % ( ttsleep ))
              time.sleep(ttsleep)
              # Readout
              looptime = time.time()-restime
              oldrestime = restime;
              ser.write(b'r')
              record = ser.readline().lstrip().rstrip()

              #ser.write(b'x')
              #time.sleep(1.0)

              restime = time.time()
              ser.write(b'x')

              records = record.split(',')  
              irecords = map(int,records)

              suma = sum(map(int,records[1:]))

              logging.info("{} events with total of {:.0f} recorded in {:.2f} since {:s}.".format(records[0], suma, looptime, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(oldrestime))))

              if ((irecords[0] > 950) and (ttsleep > 0.5)) :
                 ttsleep = (0.8*ttsleep); 
                 logging.warn("Risk of NB overflow decreasing NB readout delay to %f.", ttsleep)
              
              nbf.write(str(oldrestime) + "," + str(looptime) + "," + str(record) + "\n")
              nbf.flush()
              
              data['count'] = 1.0*float(records[0])/ttsleep
              data['sum'] = 1.0*float(suma)/ttsleep

              message = 'not set'

        except IOError as e:
          logging.critical("%s" % e)
          #self.running = False
          time.sleep(10)
          ser.close()
          nbf.close()

    ser.close()
    nbf.close()

    logging.info("NB poller thread exiting.")
    self.running = False
# end of NB_poller

  def get_nb_count(self):
    return(dv('count'))

  def get_nb_sum(self):
    return(dv('sum'))


#### main ####
if __name__ == '__main__':
  try:
    logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                      )

    logging.info('Starting NB readout')
    nb = nb_poller()
    nb.start()
    while nb.isAlive():
      time.sleep(2)
  except (KeyboardInterrupt,SystemExit):
    nb.running = False
    logging.info("NB thread asked to exit")
  
  #nb.join()

