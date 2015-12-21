#!/usr/bin/python

with open('data_log.csv') as f:
  for line in f:
    list = line.split()
    l = len(list)
    if l == 25:
      newlist = list[:13]
      newlist.extend(['nan','nan'])
      newlist.extend(list[13:])
      print ' '.join(newlist)
    elif l == 27:
      print ' '.join(list)
      True
    else:
      print ' '.join(list)
      sys.stderr.write("Not matched:\n") 
      sys.stderr.write(line)
