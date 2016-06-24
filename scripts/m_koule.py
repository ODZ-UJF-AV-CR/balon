#!/usr/bin/python
#
# Non-threaded NB poller
# 

import m_settings as g
import time
import datetime
import logging
import serial
import math
import threading

port = '/dev/ttyUSB1'

connected = False
baud = 9600

serial_port = serial.Serial(port, baud, timeout=5)

def handle_data(data):
  print(str(time.time()) + data)
  datafname = g.data_dir+"data_koule.csv"
  with open(datafname, "a") as nbf:
    nbf.write(str(time.time()) + data)
  nbf.close()

def read_from_port(ser):
  while not connected:
    #serin = ser.read()
    connected = True

    while True:
      reading = ser.readline().decode()
      handle_data(reading)

thread = threading.Thread(target=read_from_port, args=(serial_port,))
thread.start()

