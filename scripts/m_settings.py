#!/usr/bin/python
# Global settings

data_dir = '/data/balon/'
image_dir = data_dir + 'img/'

round_beat = 10

# This is for testing, triggers lpm when external power source is disconnected
#print "======================= SET REAL U LIMITS ====================="
#U_lpm = [8350, 8430] # Threshold to enter and exit the low power mode, in mV

# Flight thresholds:
U_lpm = [7000,7200]

# Modem
default_destination = "+420777642401"

#default_destination = "+420775268014"

# Testing, lower edge of interval
alt_threshold = 7000
alt_hyst = 1000

#alt_threshold = 260
#alt_hyst = 5

alt_step = 300
#print "FAKE alt step"
#alt_step = 20

# Start mode
start_timeout = 300
morituri_timeout = 300

# FAILSAFE MODE
failsafe_timeout = 7200  # s
sos_interval = 600       # s

