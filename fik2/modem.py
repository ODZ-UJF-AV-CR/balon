#!/usr/bin/python
import time
import serial

# Enable/disable LEON GSM modem
# See u-blox AT command manual.
# https://www.u-blox.com/sites/default/files/u-blox-ATCommands_Manual_(UBX-13002752).pdf
# Query status:
#  AT+CFUN?
# Enable GSM modem:
#  AT+CFUN=1
# Disable GSM modem:
#  AT+CFUN=0

# Querying signal level:
# AT+CSQ
# +CSQ: 22,99
# 
# OK

def send(data):
    try:
        ser.write(data)
    except Exception as e:
        print "Couldn't send data to serial port: %s" % str(e)
    else:
        try:
            data = ser.read(100)
        except Exception as e:
            print "Couldn't read data from serial port: %s" % str(e)
        else:
            if data:  # If data = None, timeout occurr
                n = ser.inWaiting()
                if n > 0: data += ser.read(n)
                return data

time.sleep(0.5)
ser = serial.Serial('/dev/ttyUSB0',  9600, timeout=2)
try:
   r = send('AT+CFUN?\r')
   print(r)
finally:
   ser.close()
