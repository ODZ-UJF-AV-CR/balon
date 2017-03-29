# Plot script for fik2 data log
set xdata time
set timefmt '%s'
set format x "%H:%M:%S"
set style data lines

# Primary y axis - meters
#set xlabel 'GMT time'
set ylabel 'Altitude [m]'
set ytics nomirror
set y2label 'Temperature [C]'
set y2tics
set y2range [0:]
set yrange [0:]
set xtics rotate

plot 'data_log.csv' using 1:4 axes x1y1 t 'Altimet altitude'

replot 'radiomodem.dat' using 1:3 with points ps 0.2 t 'Radiomodem GPS altitude'
replot 'data_log.csv' using 1:($13==3 ? $14 : -1000) with points ps 0.2 axes x1y1 t 'GPS altitude'

replot 'data_log.csv' using 1:2 axes x1y2 t 'Altimet temp'
replot 'data_log.csv' using 1:5 axes x1y2 t 'SHT25 temp'
replot 'data_log.csv' using 1:7 axes x1y2 t 'Battery temp'

set terminal png size 1024,768
set output 'fik2.png'
replot
set terminal dumb
set output

#Epoch	
# 2 T_Altimet
# 3 Pressure
# 4 Alt_Alt
# 5 T_SHT
# 6 Humidity
# 7 T_Bat
# 8 RemCap_mAh
# 9 Cap_mAh
# 10 U_mV
# 11 I_mA
# 12 Charge_pct
# 13 GPS_Fix
# 14 GPS_Alt
# 15 GPS_Lat
# 16 GPS_Lon
# 17 GPS_epx
# 18 GPS_epy
# 19 GPS_epv
