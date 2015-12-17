#!/usr/bin/python
# Global settings

data_dir = '/data/balon/'
image_dir = data_dir + 'img/'

round_beat = 5

# This is for testing, triggers lpm when external power source is disconnected
print "======================= SET REAL U LIMITS ====================="
U_lpm = [8350, 8430] # Threshold to enter and exit the low power mode, in mV

# Flight thresholds:
#U_lpm = [7000,7300]

# Modem
default_destination = "+420777642401"
