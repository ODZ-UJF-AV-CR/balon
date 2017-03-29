#!/usr/bin/perl -w
# Parses time and altitude and makes it epoch time

while ($r=<>) {
  ($hour,$minute,$second) = $r =~ /(.*):(.*):(.*)\t/;
  #print $hour,$minute,$second;
  print 1489795200 + $hour*3600+$minute*60+$second."\t".$r;
}
