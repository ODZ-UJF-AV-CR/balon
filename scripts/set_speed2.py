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

def settings(airrate, numchannels=0, aux=None):
	enter_at_mode(r1)
	query(r1, b"")
	query(r1, b"ATS2=%d" % airrate)
	if aux is not None:
		for cmd in aux:
			query(r1, cmd)
			query(r2, cmd)
	query(r1, b"ATS10=%d" % numchannels)
	query(r1, b"AT&W")
	query(r1, b"ATZ")
	time.sleep(0.5)
	query(r1, b"ATO")

def	main():
	if len(sys.argv) == 2:
		settings(int(sys.argv[1]))
		return
	if len(sys.argv) == 3:
		settings(int(sys.argv[1]), int(sys.argv[2]))
		return
	# [2, 4, 8, 16, 19, 24, 32, 64, 96, 128, 192, 250]

if __name__ == "__main__":
	main()
