import math
import sys

def fmt_settings(vals):
	return " ".join(["%s=%s" % m for m in vals])

AIRRATES = [2, 4, 8, 16, 19, 24, 32, 64, 96, 128, 192, 250]
schedule = [
	[("AIR_SPEED", air_speed), ("ECC", ecc)]
		for air_speed in AIRRATES
		for ecc in [0, 1]
]

with open(sys.argv[1], "rb") as f:
	for l in f:
		try:
			l = str(l, "ascii")
		except:
			continue
		if l[:2] != "t=":
			continue
		t = int(l[2:])
		if t < 1500000000 or t > 1600000000:
			continue
		print(
			t, fmt_settings(
				schedule[(t//10)%len(schedule)]
		))
