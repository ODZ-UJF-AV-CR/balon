#!/usr/bin/python
#
# Threaded PCRD SPI poller
# 

import time
import datetime
import threading
import logging

pcrd_ready = True
try:
  import spidev
except ImportError:
  logging.critical('Failed to import spidev module, PCRD poller unavailable.')
  pcrd_ready = False

#### PCRD poller ####
class PCRD_poller(threading.Thread):
  def __init__(self):
      logging.debug("PCRD poller thread is initializing.")
      threading.Thread.__init__(self)
      self.running = True
      self.name = 'PCRD'

  def run(self):
    logging.debug("Thread is starting.")
    try:
      spi = spidev.SpiDev() # create a spi object
      spi.open(1, 0) # open spi port 0, device (CS) 1
    except:
      logging.critical('PCRD SPI object could not be created.')
      self.running = False

    try:
      #spi.mode = 2
      #spi.bits_per_word = 8
      #spi.cshigh = False
      bits = 13	                                                                # number of bits from A/D
      while self.running:
        channels = [0] * (2**bits)						# number of channels
        for n in range(50000):							# number of measurements
            resp = spi.readbytes(2)						# read word from A/D converter through SPI
            channels[(resp[0] << (bits - 8)) | (resp[1] >> (16 - bits))] += 1	# increment a channel addressed by 13 bits index
            time.sleep(0.00001) 						# sleep (loop 100 us)	
        print datetime.datetime.now(), channels[:1000]				# print first 1000 channels

    except KeyboardInterrupt, SystemExit: 
      spi.close()
      self.running = False

    logging.debug("Thread is exiting.")

#### main ####
if __name__ == '__main__':
  logging.info('Starting PCRD readout')
  if pcrd_ready:
    pcrd = PCRD_poller()
    pcrd.start()
    pcrd.join()
