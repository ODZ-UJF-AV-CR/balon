#!/usr/bin/perl -w
use Time::Local;
use warnings;
   
while ($r = <>) {
  if ((@a) = $r =~ /\$GPGGA,([0-9.]+),0*([0-9.]+),N,0*([0-9.]+),E,[12],\d+,[0-9.]+,0*([0-9.]+),.*/)
  {
    if (($h,$m,$s) = $a[0] =~ /(\d\d)(\d\d)([0-9.]+)/) {
      $time = join(':',($h,$m,$s));
      $a[0] = $time; 
      print(join("\t",@a)."\n");
    } else {
      print('FAIL: '.chomp($r)."\n");
    }
  }
}
