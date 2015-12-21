#!/usr/bin/python
import time
import calendar
import re

# Split on reverse time warps
last_epoch=-1
with open('pcrd_cleaned.csv') as f:
  for line in f:
    list = line.split()
    # If we have a GPS time fix
    try:
      epoch = float(list[0])
      if (last_epoch == -1):
        last_epoch = epoch
      elif epoch >= last_epoch:
        last_epoch = epoch
      else:
        print "#-- boot --"
        last_epoch = epoch
    except ValueError:
      pass

    list.insert(0,'nan ')
    print ' '.join(list)
