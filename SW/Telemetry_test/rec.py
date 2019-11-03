#!/usr/bin/env python3

import serial
import time
import random
import sys
import math

def wait_for_phase(interval, no):
	m = float(time.time())/interval
	next_phase = (int(math.ceil(m))) % no
	time.sleep((1.0 - m%1.0)*interval)
	return next_phase

r1 = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=0)
#r2 = serial.Serial("/dev/ttyUSB1", baudrate=57600, timeout=0)

def query(r, cmd):
	r.write(cmd + b"\r")
	time.sleep(0.1)
	reply = r.read(100)
	print(r.port, cmd, reply, file=sys.stderr)
	return reply

def enter_at_mode(r):
	query(r, b"ATO")
	time.sleep(0.2)
	for _ in range(3):
		print("sending +++ to %s" % r.port, file=sys.stderr)
		r.write(b"+++")
		time.sleep(0.1)
		r.read(16)
		time.sleep(1.0)
		maybe_ok = r.read(16).strip()
		if maybe_ok == b"OK":
			print("AT mode entered", file=sys.stderr)
			return True
	return False

translate = {
	'ECC': 'ATS5',
	'AIR_SPEED': 'ATS2',
	'NUM_CHANNELS': 'ATS10'
}

def settings(target):
	enter_at_mode(r1)
	query(r1, b"")
	for key, val in target:
		key = translate.get(key, key)
		cmd = bytes("%s=%s" % (key, val), "ascii")
		query(r1, cmd)
	query(r1, b"AT&W")
	query(r1, b"ATZ")
	time.sleep(0.5)
	query(r1, b"ATO")

def test():
	time.sleep(0.2)

	a2b_hits, b2a_hits = 0, 0
	no_of_tries = 5

	for _ in range(no_of_tries):
		r1.read(40);r2.read(40)
		sys.stderr.write("."); sys.stderr.flush()
		a2b = bytes([random.getrandbits(8) for _ in range(8)])
		r1.write(a2b)
		time.sleep(0.5)
		a2b_hits += a2b == r2.read(8)
	sys.stderr.write(" (%d/%d)\n" % (a2b_hits, no_of_tries))
	return (a2b_hits)

AIRRATES = [2, 4, 8, 16, 19, 24, 32, 64, 96, 128, 192, 250]

def fmt_settings(vals):
	return " ".join(["%s=%s" % m for m in vals])

def	main():
	if len(sys.argv) == 2:
		settings(int(sys.argv[1]))
		return
	if len(sys.argv) == 3:
		settings(int(sys.argv[1]), int(sys.argv[2]))
		return

	results = dict()

	schedule = [
		[("AIR_SPEED", air_speed), ("ECC", ecc)]
			for air_speed in AIRRATES
			for ecc in [0, 1]
	]

	while True:
		m = wait_for_phase(10.0, len(schedule))
		t = time.time()
		item = schedule[m]
		("settings", fmt_settings(item))
		settings(item)
		print("sleep", file=sys.stderr)
		time.sleep(max(t+6-time.time(),0))
		print("done", file=sys.stderr)
		time.sleep(1)
		sys.stdout.buffer.write(r1.read(16))
		time.sleep(1)
		sys.stdout.buffer.write(r1.read(16))
		time.sleep(1)
		sys.stdout.buffer.write(r1.read(16))
		time.sleep(0.5)
		sys.stdout.buffer.write(r1.read(16))
		sys.stdout.buffer.flush()

if __name__ == "__main__":
	main()
