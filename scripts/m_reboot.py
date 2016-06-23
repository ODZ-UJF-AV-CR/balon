#!/usr/bin/python
import m_settings as g
import logging
import time

fname='/data/balon/boot_times.csv'

def get_boot_times():
  boot_times = []
  try:
    with open(fname, 'r') as f:
      for line in f:
        boot_times.append(line.rstrip())
    return(boot_times)
  except IOError:
    return boot_times

def get_n_boot_times():
  boot_times = []
  try:
    with open(fname, 'r') as f:
      for line in f:
        boot_times.append(line.rstrip())
    return(len(boot_times))
  except IOError:
    return 0

def append_boot_time():
  try:
    with open(fname, 'a') as f:
      f.write('%s\n' % str(time.time()))
    logging.debug('Boot time appended to list')
  except IOError as err:
    logging.error('Failure: {0}'.format(err))

def write_boot_times(boot_times):
  try:
    with open(fname, 'w') as f:
      for line in boot_times:
        f.write('%s\n' % line)
  except IOError as err:
    logging.error('Failure: {0}'.format(err))

def replace_last_boot_time():
  boot_times = get_boot_times()

  if len(boot_times) > 0:
    boot_times.pop()

  boot_times.append(time.time()) 
  write_boot_times(boot_times)
  logging.warn('Boot time list updated.')
      

##########################################################333
if __name__ == '__main__':
  print get_boot_times()
  append_boot_time()
  while True:
    replace_last_boot_time()
    print get_boot_times()
    time.sleep(1)
