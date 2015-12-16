#!/usr/bin/python
#
# Threaded PCRD SPI poller
# 

import time
import datetime
import threading
import logging
import spidev
import math

def channels_summary(channels):
  # Prebinovana a preskalovana data z kanalu do histogramu, v nule je suma
  if (len(channels) < 1):
    logging.error('No data read from PCRD?')
    return('FAIL')

  bins = 30 
  binwidth = float(len(channels))/(bins)
  aggr = [0] * (bins+1)
  #print '%d bins %.1f ch each' % (bins, binwidth)

  for ch in range(1,len(channels)-1):
    binnr=int(math.floor(ch/binwidth))
    if binnr > bins-1:
      logging.error('Binning issue %d' % binnr)
      binnr = bins-1
    #aggr[binnr+1]+=ch*channels[ch]
    #aggr[0]+=ch*channels[ch]
    aggr[binnr+1]+=channels[ch]
    aggr[0]+=(1+binnr)*channels[ch]
  
  return(aggr)

#### PCRD poller ####
class PCRD_poller(threading.Thread):
  # Default data dir
  data_dir = './'
  def __init__(self):
      logging.info("PCRD poller thread is initializing.")
      threading.Thread.__init__(self)
      self.running = True
      self.name = 'PCRD'

  def run(self):
    global sensors
    logging.info("Thread is starting.")
    try:
      spi = spidev.SpiDev() # create a spi object
      spi.open(1, 0) # open spi port 0, device (CS) 1
    except IOError as e:
      logging.critical('PCRD SPI object could not be created: %s' % e)
      self.running = False

    try:
      datafname = self.data_dir+"data_pcrd.csv"
      logging.info('PCRD data will be appended to: %s' % (datafname))
      with open(datafname, "a") as pf:
        #spi.mode = 2
        #spi.bits_per_word = 8
        #spi.cshigh = False
        bits = 13	                                                        # number of bits from A/D
        while self.running:
          roundstart = time.time()
          channels = [0] * (2**bits)						# number of channels
          for n in range(50000):							# number of measurements
            resp = spi.readbytes(2)						# read word from A/D converter through SPI
            channels[(resp[0] << (bits - 8)) | (resp[1] >> (16 - bits))] += 1	# increment a channel addressed by 13 bits index
            time.sleep(0.00001) 						# sleep (loop 100 us)	
          #print datetime.datetime.now(), channels				# print all channels
          pf.write('%s %s %s ' % (str(time.time()), str(time.time()-roundstart), str(datetime.datetime.now())))
          pf.write((' %s\n' % (' '.join(str(x) for x in channels))))
          pf.flush()
          message = str(channels[:30])    # print first 30 channels
          logging.info('Ch:  ' + message)
          logging.info('Sum: ' + str(channels_summary(channels)))

    except IOError as e:
      logging.critical("%s" % e)
      self.running = False

    pf.close()

    logging.info("PCRD poller thread exiting.")
    spi.close()
    self.running = False
# end of PCRD_poller

#### main ####
if __name__ == '__main__':
  try:
    logging.basicConfig(level=logging.INFO,
                      format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                      )

    logging.info('Starting PCRD readout')
    pcrd = PCRD_poller()
    pcrd.start()
    while pcrd.isAlive():
      time.sleep(2)
  except (KeyboardInterrupt,SystemExit):
    pcrd.running = False
    logging.info("PCRD thread asked to exit")
 
  pcrd.join()

