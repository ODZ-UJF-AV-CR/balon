#!/usr/bin/python

import csv
import re

with open('data_nb.csv') as csvfile:
  reader = csv.reader(csvfile, delimiter='\t', quotechar='|')
  for line in reader:
    if (line[0] != 'Epoch') and (len(line) > 8):
      header = line[0:7]
      events = line[8:]
      for ev in events:
        row = [ev] + header
        print ','.join(row)
