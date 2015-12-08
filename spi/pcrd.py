#!/usr/bin/python
import spidev
import time
import datetime

spi = spidev.SpiDev() # create a spi object
spi.open(1, 0) # open spi port 0, device (CS) 1
try:
    #spi.mode = 2
    #spi.bits_per_word = 8
    #spi.cshigh = False
    bits = 13																# number of bits from A/D
    while True:
        channels = [0] * (2**bits)											# number of channels
        for n in range(50000):												# number of measurements
            resp = spi.readbytes(2)											# read word from A/D converter through SPI
            channels[(resp[0] << (bits - 8)) | (resp[1] >> (16 - bits))] += 1	# increment a channel addressed by 13 bits index
            time.sleep(0.00001) 											# sleep (loop 100 us)	
        print datetime.datetime.now(), channels[:1000]						# print first 1000 channels
        #time.sleep(0.1) # sleep for 0.1 second
    #end while

except KeyboardInterrupt: 
    spi.close()
#end try     
