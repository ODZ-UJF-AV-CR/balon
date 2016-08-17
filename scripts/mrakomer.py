
#!/usr/bin/python
#
# Mrakomer poller
# 

import m_settings as g
import time
import datetime
import logging
import serial
import math
import threading
from pymlab import config


port = '/dev/ttyUSB0'

baud = 2400

serial_port = serial.Serial(port, baud, timeout=5)

cfg = 	config.Config(
		    i2c = {
		        "port": 1,
		    },
		    bus = [
		        {
		            "name":          "altimet",
		            "type":        "altimet01",
		        },
		    ],
		)

cfg.initialize()
alt = cfg.get_device("altimet")
time.sleep(0.5)


def handle_data(data):
	print data,
	datafname = '/home/odroid/mrakomer/station/data/' + str(time.strftime("%Y%m%d%H0000000")) + "_LS-M0_meta" + ".csv"
	if int(time.strftime('%Y')) >= 2016:
		with open(datafname, "a") as nbf:
			nbf.write(data)
		nbf.close()

while True:
	reading = serial_port.readline().rstrip()
	values = reading.split(' ')
	if (len(values) == 18):
		(t1, p1) = alt.get_tp()
		#print values,
		handle_data(str(time.time()) + ','
		+ values[1] + ',' 
		+ str(round(t1,2)) + ',' 
		+ str(round(p1,1)) + ',' 
		+ str(round(float(values[2])/100,2)) + ',' 
		+ str(round(float(values[3])/100,2)) + ',' 
		+ str(round(float(values[4])/100,2)) + ',' 
		#+ str(round(float(values[5])/100,2)) + ',' 
		+ values[6] + ',' 
		#+ values[7] + ',' 
		+ values[8] #+ ',' 
		#+ values[9] + ',' 
		#+ values[10] + ',' 
		#+ values[11] + ',' 
		#+ values[12] + ',' 
		#+ values[13] + ',' 
		#+ values[14] + ',' 
		#+ values[15] + ',' 
		#+ values[16] + ',' 
		#+ values[17] 
		+ '\n'
		)
		 

