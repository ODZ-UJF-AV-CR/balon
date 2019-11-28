#!/usr/bin/env python3

import serial
import time
import random
import sys

r1 = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=0)

def query(r, cmd):
	r.write(cmd + b"\r")
	time.sleep(0.1)
	reply = r.read(100)
	print(r.port, cmd, reply)
	return reply

def enter_at_mode(r):
	query(r, b"ATO")
	time.sleep(0.2)
	for _ in range(3):
		print("sending +++ to %s" % r.port)
		r.write(b"+++")
		time.sleep(0.1)
		r.read(16)
		time.sleep(1.0)
		maybe_ok = r.read(16).strip()
		if maybe_ok == b"OK":
			print("AT mode entered")
			return True
	return False

def settings():
	enter_at_mode(r1)
	query(r1, b"")
	query(r1, b"ATS0=26")
	query(r1, b"ATS1=57")
	query(r1, b"ATS2=2") 	# [2, 4, 8, 16, 19, 24, 32, 64, 96, 128, 192, 250]
	query(r1, b"ATS3=25")
	query(r1, b"ATS4=20")
	query(r1, b"ATS5=1")
	query(r1, b"ATS6=1")		 ## 1 - mavlink activated
	query(r1, b"ATS7=0")
	query(r1, b"ATS8=434050")
	query(r1, b"ATS9=434051")
	query(r1, b"ATS10=10")
	query(r1, b"ATS11=100")
	query(r1, b"ATS12=0")
	query(r1, b"ATS13=0")
	query(r1, b"ATS14=0")
	query(r1, b"ATS15=131")
	query(r1, b"ATS16=0")
	query(r1, b"AT&W")
	query(r1, b"ATZ")
	time.sleep(0.5)
	query(r1, b"ATO")

def	main():
	settings()
	return

if __name__ == "__main__":
	main()
