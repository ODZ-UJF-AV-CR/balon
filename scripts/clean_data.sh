#!/bin/bash
data_dir=/data/balon
echo -n Remove all logs and img dir in: ${data_dir} [y/n]?\ 
read r
if [ x$r == "xy" ]; then
  cd $data_dir || exit 1
  rm -v data_*.csv monitor.log 
  rm -vrf img
else
  echo Ok, not removing anything.
fi

