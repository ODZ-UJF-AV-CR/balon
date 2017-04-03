# Plot script for fik2 data log
set xdata time
set timefmt '%H:%M:%S'
set format x "%H:%M:%S"
set style data points

# Primary y axis - meters
#set xlabel 'GMT time'
set ylabel 'Altitude [m]'
set ytics nomirror
set yrange [0:]
set xtics rotate

plot 'LetFik2_HabHub_data.csv' using 1:4 axes x1y1 t 'Altitude'


#set terminal png size 1024,768
#set output 'fik2.png'
#replot
#set terminal dumb
#set output

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
