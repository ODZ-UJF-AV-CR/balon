#!/usr/bin/python
import time
import serial

port = "/dev/ttyUSB0"

# Enable/disable LEON GSM modem
# See u-blox AT command manual.
# https://www.u-blox.com/sites/default/files/u-blox-ATCommands_Manual_(UBX-13002752).pdf
# Query status:
#  AT+CFUN?
# Enable GPS modem:
#  AT+CFUN=1
# Disable GPS modem:
#  AT+CFUN=0

# Querying signal level:
# AT+CSQ
# +CSQ: 22,99
# 
# OK



m = serial.Serial(port,  9600, timeout=5)
try:
    time.sleep(0.5)
    m.write(b'AT+CFUN=0\r')
    line = m.readline(5)
    print(line)
    line = m.readline(5)
    print(line)
finally:
    m.close()
