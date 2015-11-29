#!/usr/bin/python
import spidev
import time
import os


GPIO_MODE_PATH= os.path.normpath('/sys/class/gpio/gpio204/direction')
GPIO_PIN_PATH=os.path.normpath('/sys/class/gpio/gpio204/value')
GPIO_EDGE_PATH=os.path.normpath('/sys/class/gpio/gpio204/edge')
GPIO_EXPORT_PATH=os.path.normpath('/sys/class/gpio/export')



def writepin(pin_value):
    pin = open("/sys/class/gpio/gpio204/value","w")
    pin.write(pin_value)
    pin.close()


try:
    file = open(GPIO_EXPORT_PATH, 'w') 
    file.write("204")          ## export the pin to the usermode
    file.close()                  


    file = open(GPIO_MODE_PATH, 'r+') 
    file.write("out")          ## make the pin as output
    file.close()                  
except:
    print "reinit..."


spi = spidev.SpiDev() # create spi object
spi.open(1, 0) # open spi port 0, device (CS) 1
try:
    #spi.mode = 2
    #spi.bits_per_word = 8
    #spi.cshigh = False
    writepin("1")
    while True:
        #resp = spi.readbytes(2)
        #resp = spi.xfer([0xAA,0x55,0xAA,0x55],10000000,0) # transfer one byte
        for n in range(7000):
            writepin("0")
            #writepin("0")
            time.sleep(0.0001)  # cca 250 us
            pin = open("/sys/class/gpio/gpio204/value","w")
            pin.write("1")
            resp = spi.readbytes(2)
            pin.close()
        time.sleep(0.1) # sleep for 0.1 seconds
        #end while
except KeyboardInterrupt: 
    spi.close()
    pin.close()
#end try     
