#!/usr/bin/python
import time
import calendar
import re
import sys

rtccorrection = 0 
with open('pcrd_split.csv') as f:
  for line in f:
    items = line.split()
    # If first column is a correction factor
    
    if (items[0] == 'nan'): 
      pass
    else:
      try:
        tcorrf = float(items[0])
      except:
        sys.stderr.write('Error' + line[:80] + "\n")

    rtcepoch = float(items[1])
    corrected = time.strftime('%H:%M:%S', time.gmtime(tcorrf + rtcepoch))
    items.pop(4)
    items.pop(3)
    items.pop(1)
    items[0] = corrected

    print ' '.join(items)
