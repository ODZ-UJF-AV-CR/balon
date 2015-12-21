#!/usr/bin/python
import time
import calendar
import re

rtccorrection = 0 
with open('data_corrected.csv') as f:
  for line in f:
    list = line.split()
    # If we have a GPS time fix
    tre = re.match('(\d+:\d+:\d+)([.]?\d*)', str(list[1]))
    if tre:
      gpstimepart = tre.group(1)
      gpstimestring = "19 12 2015 "+gpstimepart

      try:
        gpstimestruct = time.strptime(gpstimestring, "%d %m %Y %H:%M:%S")
        #print "OK for " + timestring
        gpsepoch = calendar.timegm(gpstimestruct)
        rtcepoch = float(list[0])
        rtccorrection = gpsepoch-rtcepoch
        
      except ValueError:
        print "Fail for " + timestring
    
    try:
      corrected_rtc = time.strftime('%H:%M:%S', time.gmtime(float(list[0])+rtccorrection))
      list.insert(0, corrected_rtc) 
    except ValueError:
      list.insert(0, 'RTC_Corrected')

    print ' '.join(list)
