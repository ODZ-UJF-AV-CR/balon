from pymlab import config
from gps import gps, WATCH_ENABLE
import os
import subprocess
import logging
import threading
import math
import time
import copy
import Queue as qu
import m_i2c
import m_settings as g


devnull = open(os.devnull, 'w')


class StateDict:
	def __init__(self):
		pass

	def __setitem__(self, key, val):
		self.__dict__[key] = val
		self.__dict__[key + "_Epoch"] = self["Epoch"]

	def __getitem__(self, key):
		return self.__dict__[key]

	def __contains__(self, key):
		return key in self.__dict__

	def have(self, key, max_age=1.0):
		return key in self and self[key + "_Epoch"] >= self["Epoch"] - max_age

	def get(self, key, d):
		if key in self:
			return self[key]
		else:
			return d

	def copy(self):
		return copy.copy(self)


class GpsPoller(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.setDaemon(True)
		self.gpsd = gps(mode=WATCH_ENABLE)
		self.running = True
		self.qu = qu.Queue()

	def run(self):
		while self.running:
			self.qu.put(self.gpsd.next())

	@staticmethod
	def read_tpv_message(msg, st):
		logging.info("GPS TPV message: %s" % msg)

		b = [
			("GPS_Fix", "mode"),
			("GPS_Alt", "alt"),
			("GPS_Lat", "lat"),
			("GPS_Lon", "lon"),
			("GPS_epx", "epx"),
			("GPS_epy", "epy"),
			("GPS_epv", "epv")
		]

		for st_key, msg_key in b:
			if msg_key in msg:
				st[st_key] = msg[msg_key]

	def get_gps_data(self, st):
		try:
			while True:
				msg = self.qu.get_nowait()

				if "class" not in msg or msg["class"] != "TPV":
					continue

				self.read_tpv_message(msg, st)

		except qu.Empty:
			pass

		columns = ["GPS_Fix", "GPS_Alt", "GPS_Lat", "GPS_Lon", "GPS_epx", "GPS_epy", "GPS_epv"]

		return {'header': "\t".join(columns) + "\t",
			'record': "\t".join(["%s" % st.get(k, 0) for k in columns])+"\t"}


def height(state):
	if state["GPS_Fix"] > 2 and state.have("GPS_Alt", max_age=10.0):
		return state["GPS_Alt"]

	if state.have("Altimet_Alt") and not math.isnan(state["Altimet_Alt"]):
		return state["Altimet_Alt"]

	return 0


def sms_trigger():
	global radio_okay

	last_sms = state = (yield).copy()
	last_sms["Epoch"] = 0

	while True:
		while True:
			state = yield

			if height(state) > g.alt_radio_off:
				logging.warning("Should turn GSM radio off.")
				subprocess.Popen(["/home/odroid/git/balon/fik2/modem.py", "AT+CFUN=0"],
						 stdout=devnull, stderr=devnull)
				

				while height(state) > g.alt_radio_on:
					state = yield

				logging.warning("Should turn GSM radio on.")

				radio_okay = False

				while True:
					try:
						logging.warning("running modem.py AT+CFUN=16")
						p = subprocess.Popen(["/home/odroid/git/balon/fik2/modem.py", "AT+CFUN=16"], stdout=devnull, stderr=devnull)	
						while p.poll() is None:
							yield

						if p.returncode == 0:
							break

						logging.error("modem.py non-zero return code")
					except OSError as e:
						logging.error("turning GSM radio on: %s" % e)

				
				logging.warning("GSM radio ok")
				radio_okay = True
				continue
					

			if (state["Epoch"] - last_sms["Epoch"]) < g.sms_delay_min:
				continue

			if (state["Epoch"] - last_sms["Epoch"]) > g.sms_delay_max:
				break

			if abs(height(state) - height(last_sms)) > g.alt_diff_sms_trigger:
				break

		logging.info("------------- SMS triggered. -----------------")
		# TODO
		last_sms = state.copy()

		payload = "%sA%05.0fG%05.0fF%dC%04dV%04d %s%08.5f,%08.5f" % (
			time.strftime("%H-%M-%S", time.gmtime()),
			state.get("Altimet_Alt", 0),
			state.get("GPS_Alt", 0),
			state.get("GPS_Fix", 0),
			state.get("Bat_RemCap", 0),
			state.get("Bat_V", 0),
			"http://maps.google.com/?q=",
			state.get("GPS_Lat", 0),
			state.get("GPS_Lon", 0)
		)

		try:
			subprocess.Popen(["gammu", "sendsms", "TEXT",
					  g.sms_phone_number, "-text", payload],
					 stdout=devnull, stderr=devnull)
		except OSError as e:
			logging.error("sending SMS: %s" % e)

		logging.info("Payload: %s" % payload)


def readout():
	gpsp = GpsPoller()
	gpsp.start()

	state = StateDict()

	with open(g.data_dir+"data_log.csv", "a") as f:
		write_header = True
	
		while True:
			status_i2c = m_i2c.get_i2c_data(state)
			status_gps = gpsp.get_gps_data(state)

			try:
				if write_header:
					f.write("Epoch\t" + status_i2c['header'] + status_gps['header'] + "\n")
					write_header = False
				f.write(("%d\t" % state["Epoch"]) + status_i2c['record'] + status_gps['record'] + "\n")
				f.flush()
			except IOError as e:
				logging.error("writing CSV: %s" % e)
				# TODO
				pass

			yield state


def main():
	global radio_okay
	radio_okay = True

	logging.basicConfig(level=logging.INFO,
	#	format='[%(levelname)s] %(message)s',
   		format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
		filename=time.strftime("/data/balon/monitor-%F-%H%M%S.log", time.gmtime())
	)

	trigger = sms_trigger()
	next(trigger)

	for s in readout():
		trigger.send(s)

		if not radio_okay:
			continue

		try:
			with open("/dev/ttyUSB1", "w") as wd:
				wd.write("k")
		except IOError:
			pass
		

if __name__ == "__main__":
	main()

