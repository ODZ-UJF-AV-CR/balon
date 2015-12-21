#!/usr/bin/python
import time
import math
import calendar
import re
import sys

def channels_summary(channels):
  # Prebinovana a preskalovana data z kanalu do histogramu, v nule je suma
  if (len(channels) < 1):
    logging.error('No data read from PCRD?')
    return('FAIL')

  bins = 30
  binwidth = float(len(channels))/(bins)
  aggr = [0] * (bins+2)
  #print '%d bins %.1f ch each' % (bins, binwidth)

  for ch in range(1,len(channels)-1):
    binnr=int(math.floor(ch/binwidth))
    if binnr > bins-1:
      logging.error('Binning issue %d' % binnr)
      binnr = bins-1
    #aggr[binnr+1]+=ch*channels[ch]
    #aggr[0]+=ch*channels[ch]
    try:
      aggr[binnr+2]+=float(channels[ch])
      aggr[0]+=(1+binnr)*float(channels[ch])
      aggr[1]+= (float(channels[ch]))
    except ValueError:
      print channels[ch]

  return(aggr)

linenr = 0
avg_over = 24

with open('pcrd_final.csv') as f:
  print "#Time[s] Duration[s] WeightedSum Sum AvgWeighted AvgSum"
  for line in f:
    linenr += 1
    items = line.split(' ')
    rebinned = channels_summary(items[2:])
    if linenr < 2:
      avg = list(rebinned)
    
    if rebinned[0] < 70:
      for i in range(0,len(rebinned)-1):
        avg[i] = (avg[i]*(avg_over - 1.0) + rebinned[i])/avg_over
  
    sys.stdout.write(' '.join(items[0:2]))
    sys.stdout.write(' ' + str(rebinned[0]))
    sys.stdout.write(' ' + str(rebinned[1]))
    sys.stdout.write(' ' + str(avg[0]))
    sys.stdout.write(' ' + str(avg[1]))
    sys.stdout.write("\n")
