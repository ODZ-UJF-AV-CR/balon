set xdata time
set timefmt "%H:%M:%S"
set format x "%H:%M"
set xlabel 'UTC Time [h:m]'
set ylabel 'Altitude [m]'
set datafile missing 'nan'
set grid
set ytics 0,1000
set yrange [0:33000]
set key left top

# This plots barometric altitude from pressure using ICAO simplified model
#plot 'data_final.csv' using 1:(44330.76923076923*(1-(($19/101325.0)**(1/5.255)))) with points pointtype 7 pointsize 0.4 t 'Barometric altitude'
plot 'data_final.csv' using 1:20 with points pointtype 7 pointsize 1 t 'Barometric altitude'
replot '../gps/kovarova_gps.csv' using 1:4 with points pointtype 7 pointsize 0.7 t 'SkyFox GPS' 
replot 'utc-gps.dat' using 1:2 with points pointtype 7 pointsize 0.5 t 'System GPS'

set terminal png size 900,600
set output 'gps-altitudes.png'
replot
set terminal x11
set output

