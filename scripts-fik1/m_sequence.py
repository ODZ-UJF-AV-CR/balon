#!/usr/bin/python
import glob
import re
import m_settings as g
import logging

def find_last_used_counter():
  fnseq = 1
  file_re = re.compile('^.*/0?(\d+)\.jpg$')
  for jpeg in glob.iglob(g.image_dir + '*.jpg'):
    m = file_re.match(jpeg)
    if m:
      jpegno = int(m.group(1))
      if fnseq < jpegno:
        fnseq = jpegno
    else:
      logging.error('Strange file name: %s' % jpeg)
  return(fnseq)

def get_next_image_fname():
  global fnseq
  fnseq += 1
  return('%s%06d.jpg' % (g.image_dir, fnseq))

### Initialization ###
fnseq = find_last_used_counter()
if fnseq > 1:
  fnseq += 2

##########################################################333
if __name__ == '__main__':
  print get_next_image_fname()
  print get_next_image_fname()
  print get_next_image_fname()
