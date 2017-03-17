#!/bin/bash

trap 'pkill -TERM -P $$' SIGINT

function find_last_of {
	FNAME=`find $1* | sort | tail -n1`
}

echo -e "\n======\nBezi sluzby?\n\n"
service balon status
sh -c 'sleep 10'

echo -e "\n======\ndata_log.csv?\n\n"
sh -c 'tail -n 2 -f /data/balon/data_log.csv'

echo -e "\n======\ndata_koule.csv?\n\n"
sh -c 'tail -n 2 -f /data/balon/data_koule.csv'

echo -e "\n======\nmonitor.log?\n\n"
find_last_of "/data/balon/monitor-"
tail -n 2 -f $FNAME

echo -e "\n======\nRoste video soubor?\n\n"

find_last_of "/data/balon/video/"

while sh -mc 'sleep 0.3'; do
	ls -la $FNAME
done

