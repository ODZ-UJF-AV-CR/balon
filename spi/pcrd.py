#!/usr/bin/python
import spidev
import time
import datetime

spi = spidev.SpiDev() # create spi object
spi.open(1, 0) # open spi port 0, device (CS) 1
try:
    #spi.mode = 2
    #spi.bits_per_word = 8
    #spi.cshigh = False
    while True:
        channels = [0] * 512
        #resp = spi.readbytes(2)
        #resp = spi.xfer([0xAA,0x55,0xAA,0x55],10000000,0) # transfer one byte
        for n in range(10000):
            resp = spi.readbytes(2)
            channels[(resp[0] << 1) | (resp[1] >> 7)] += 1
            time.sleep(0.00001) # sleep (loop 100 us)
        print datetime.datetime.now(), channels
        #time.sleep(0.1) # sleep for 0.1 seconds
        #end while
except KeyboardInterrupt: 
    spi.close()
#end try     
