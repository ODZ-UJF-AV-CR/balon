#!/usr/bin/python
import sys
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

def send(cmd):
    with serial.Serial("/dev/ttyUSB0", 9600, timeout=10) as s:
	s.write(cmd + "\r\n")

	while True:
		line = s.readline()
		if line is None:
			break
		line = line.strip().upper()

		print line		

		if line == "OK":
			return True

		if line == "ERROR":
			return False

	return False


def main():
	if not send(sys.argv[1]):
		sys.exit(1)

if __name__ == "__main__":
	main()

