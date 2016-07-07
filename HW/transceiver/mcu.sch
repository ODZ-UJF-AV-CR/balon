EESchema Schematic File Version 2
LIBS:modballoon-rescue
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:Balon
LIBS:mic4680-3
LIBS:sam4sd16
LIBS:sam_jtag
LIBS:tps22945dckr
LIBS:fa-238v-12mhz
LIBS:sma
LIBS:si4463
LIBS:7q-26
LIBS:as193
LIBS:sp5189z
LIBS:spf5189z
LIBS:saw
LIBS:rf5110g
LIBS:modballoon-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 3 4
Title ""
Date "4 may 2016"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text HLabel 1100 1850 0    60   Input ~ 0
3V3
Text HLabel 5800 4900 2    60   Output ~ 0
TxOn
Text HLabel 4000 6100 3    60   Output ~ 0
SDN
Text HLabel 4500 6100 3    60   Output ~ 0
nSEL
Text HLabel 3900 6100 3    60   Output ~ 0
SDI
Text HLabel 4400 6100 3    60   Input ~ 0
SDO
Text HLabel 3800 6100 3    60   Output ~ 0
SCLK
Text HLabel 3600 6100 3    60   Output ~ 0
nIRQ
Text HLabel 4900 6100 3    60   Output ~ 0
GPSOn
Text HLabel 4700 6100 3    60   Input ~ 0
GPSUartRx
Text HLabel 1100 3050 0    60   Input ~ 0
Vbat
Text HLabel 2550 4000 0    60   Input ~ 0
UartRx
Text HLabel 2550 4100 0    60   Output ~ 0
UartTx
Text HLabel 5800 4100 2    60   BiDi ~ 0
SDA
Text HLabel 5800 4800 2    60   Output ~ 0
SCL
Text HLabel 5800 3600 2    60   BiDi ~ 0
GPIO0
Text HLabel 5800 3700 2    60   BiDi ~ 0
GPIO1
Text HLabel 5800 4000 2    60   BiDi ~ 0
GPIO2
$Comp
L SAM4SD16 DD4
U 1 1 5728C394
P 3650 2950
F 0 "DD4" H 5150 3000 60  0000 C CNN
F 1 "SAM4SD16" H 5300 2900 60  0000 C CNN
F 2 "Housings_QFP:LQFP-64_10x10mm_Pitch0.5mm" H 3550 2950 60  0001 C CNN
F 3 "" H 3550 2950 60  0000 C CNN
	1    3650 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4500 6100 4500 5900
Wire Wire Line
	4400 6100 4400 5900
Wire Wire Line
	4000 6100 4000 5900
Wire Wire Line
	3900 6100 3900 5900
Wire Wire Line
	3800 6100 3800 5900
Wire Wire Line
	3600 6100 3600 5900
Wire Wire Line
	4700 6100 4700 5900
Wire Wire Line
	2550 4000 2750 4000
Wire Wire Line
	2750 4100 2550 4100
Wire Wire Line
	5800 4100 5600 4100
Wire Wire Line
	5600 4800 5800 4800
Wire Wire Line
	5800 3600 5600 3600
Wire Wire Line
	5800 3700 5600 3700
Wire Wire Line
	5800 4000 5600 4000
Wire Wire Line
	5800 4900 5600 4900
Wire Wire Line
	4900 6100 4900 5900
Wire Wire Line
	4100 6600 4100 5900
Wire Wire Line
	2050 6600 4100 6600
Wire Wire Line
	2050 1950 2050 6800
Wire Wire Line
	2050 4700 2750 4700
Wire Wire Line
	2050 4300 2750 4300
Connection ~ 2050 4700
Wire Wire Line
	2050 3900 2750 3900
Connection ~ 2050 4300
Wire Wire Line
	4400 2850 4400 1950
Wire Wire Line
	4400 1950 2050 1950
Connection ~ 2050 3900
$Comp
L INDUCTOR L7
U 1 1 5728C78C
P 2450 2200
F 0 "L7" V 2400 2200 40  0000 C CNN
F 1 "74279204" V 2550 2200 40  0000 C CNN
F 2 "Capacitors_SMD:C_0805" H 2450 2200 60  0001 C CNN
F 3 "~" H 2450 2200 60  0000 C CNN
	1    2450 2200
	0    1    1    0   
$EndComp
$Comp
L C-RESCUE-modballoon C17
U 1 1 5728C7AA
P 2850 2500
F 0 "C17" H 2850 2600 40  0000 L CNN
F 1 "1M" H 2856 2415 40  0000 L CNN
F 2 "Capacitors_SMD:C_0603" H 2888 2350 30  0001 C CNN
F 3 "~" H 2850 2500 60  0000 C CNN
	1    2850 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	2150 2200 2050 2200
Connection ~ 2050 2200
Wire Wire Line
	2750 2200 3400 2200
Wire Wire Line
	2850 2200 2850 2300
Wire Wire Line
	3400 2200 3400 2850
Connection ~ 2850 2200
$Comp
L GND-RESCUE-modballoon #PWR035
U 1 1 5728C84A
P 2850 2800
F 0 "#PWR035" H 2850 2800 30  0001 C CNN
F 1 "GND" H 2850 2730 30  0001 C CNN
F 2 "" H 2850 2800 60  0000 C CNN
F 3 "" H 2850 2800 60  0000 C CNN
	1    2850 2800
	1    0    0    -1  
$EndComp
Wire Wire Line
	2850 2800 2850 2700
$Comp
L C-RESCUE-modballoon C14
U 1 1 5728C87A
P 2050 7000
F 0 "C14" H 2050 7100 40  0000 L CNN
F 1 "1M" H 2056 6915 40  0000 L CNN
F 2 "Capacitors_SMD:C_0603" H 2088 6850 30  0001 C CNN
F 3 "~" H 2050 7000 60  0000 C CNN
	1    2050 7000
	1    0    0    -1  
$EndComp
$Comp
L C-RESCUE-modballoon C15
U 1 1 5728C880
P 2400 7000
F 0 "C15" H 2400 7100 40  0000 L CNN
F 1 "M1" H 2406 6915 40  0000 L CNN
F 2 "Capacitors_SMD:C_0603" H 2438 6850 30  0001 C CNN
F 3 "~" H 2400 7000 60  0000 C CNN
	1    2400 7000
	1    0    0    -1  
$EndComp
$Comp
L C-RESCUE-modballoon C16
U 1 1 5728C8B6
P 2750 7000
F 0 "C16" H 2750 7100 40  0000 L CNN
F 1 "M1" H 2756 6915 40  0000 L CNN
F 2 "Capacitors_SMD:C_0603" H 2788 6850 30  0001 C CNN
F 3 "~" H 2750 7000 60  0000 C CNN
	1    2750 7000
	1    0    0    -1  
$EndComp
$Comp
L C-RESCUE-modballoon C18
U 1 1 5728C8BC
P 3100 7000
F 0 "C18" H 3100 7100 40  0000 L CNN
F 1 "M1" H 3106 6915 40  0000 L CNN
F 2 "Capacitors_SMD:C_0603" H 3138 6850 30  0001 C CNN
F 3 "~" H 3100 7000 60  0000 C CNN
	1    3100 7000
	1    0    0    -1  
$EndComp
Connection ~ 2050 6600
Wire Wire Line
	2400 6800 2400 6600
Connection ~ 2400 6600
Wire Wire Line
	2750 6800 2750 6600
Connection ~ 2750 6600
Wire Wire Line
	3100 6800 3100 6600
Connection ~ 3100 6600
$Comp
L GND-RESCUE-modballoon #PWR036
U 1 1 5728C981
P 2050 7400
F 0 "#PWR036" H 2050 7400 30  0001 C CNN
F 1 "GND" H 2050 7330 30  0001 C CNN
F 2 "" H 2050 7400 60  0000 C CNN
F 3 "" H 2050 7400 60  0000 C CNN
	1    2050 7400
	1    0    0    -1  
$EndComp
$Comp
L GND-RESCUE-modballoon #PWR037
U 1 1 5728C990
P 2400 7400
F 0 "#PWR037" H 2400 7400 30  0001 C CNN
F 1 "GND" H 2400 7330 30  0001 C CNN
F 2 "" H 2400 7400 60  0000 C CNN
F 3 "" H 2400 7400 60  0000 C CNN
	1    2400 7400
	1    0    0    -1  
$EndComp
$Comp
L GND-RESCUE-modballoon #PWR038
U 1 1 5728C99F
P 2750 7400
F 0 "#PWR038" H 2750 7400 30  0001 C CNN
F 1 "GND" H 2750 7330 30  0001 C CNN
F 2 "" H 2750 7400 60  0000 C CNN
F 3 "" H 2750 7400 60  0000 C CNN
	1    2750 7400
	1    0    0    -1  
$EndComp
$Comp
L GND-RESCUE-modballoon #PWR039
U 1 1 5728C9AE
P 3100 7400
F 0 "#PWR039" H 3100 7400 30  0001 C CNN
F 1 "GND" H 3100 7330 30  0001 C CNN
F 2 "" H 3100 7400 60  0000 C CNN
F 3 "" H 3100 7400 60  0000 C CNN
	1    3100 7400
	1    0    0    -1  
$EndComp
Wire Wire Line
	3100 7400 3100 7200
Wire Wire Line
	2750 7400 2750 7200
Wire Wire Line
	2400 7400 2400 7200
Wire Wire Line
	2050 7400 2050 7200
$Comp
L GND-RESCUE-modballoon #PWR040
U 1 1 5728CA88
P 3400 6000
F 0 "#PWR040" H 3400 6000 30  0001 C CNN
F 1 "GND" H 3400 5930 30  0001 C CNN
F 2 "" H 3400 6000 60  0000 C CNN
F 3 "" H 3400 6000 60  0000 C CNN
	1    3400 6000
	1    0    0    -1  
$EndComp
Wire Wire Line
	3400 6000 3400 5900
$Comp
L GND-RESCUE-modballoon #PWR041
U 1 1 5728CAC6
P 2650 3700
F 0 "#PWR041" H 2650 3700 30  0001 C CNN
F 1 "GND" H 2650 3630 30  0001 C CNN
F 2 "" H 2650 3700 60  0000 C CNN
F 3 "" H 2650 3700 60  0000 C CNN
	1    2650 3700
	0    1    1    0   
$EndComp
Wire Wire Line
	2750 3700 2650 3700
$Comp
L GND-RESCUE-modballoon #PWR042
U 1 1 5728CB05
P 3800 2750
F 0 "#PWR042" H 3800 2750 30  0001 C CNN
F 1 "GND" H 3800 2680 30  0001 C CNN
F 2 "" H 3800 2750 60  0000 C CNN
F 3 "" H 3800 2750 60  0000 C CNN
	1    3800 2750
	-1   0    0    1   
$EndComp
Wire Wire Line
	3800 2850 3800 2750
$Comp
L GND-RESCUE-modballoon #PWR043
U 1 1 5728CB45
P 5700 3800
F 0 "#PWR043" H 5700 3800 30  0001 C CNN
F 1 "GND" H 5700 3730 30  0001 C CNN
F 2 "" H 5700 3800 60  0000 C CNN
F 3 "" H 5700 3800 60  0000 C CNN
	1    5700 3800
	0    -1   -1   0   
$EndComp
Wire Wire Line
	5700 3800 5600 3800
Wire Wire Line
	3500 5900 3500 6700
Wire Wire Line
	1950 6700 6600 6700
Wire Wire Line
	1950 1850 1950 6700
Wire Wire Line
	1950 4200 2750 4200
Wire Wire Line
	6600 6700 6600 3900
Wire Wire Line
	6600 3900 5600 3900
Connection ~ 3500 6700
Wire Wire Line
	1850 1850 8650 1850
Wire Wire Line
	4000 1850 4000 2850
Connection ~ 1950 4200
$Comp
L INDUCTOR L6
U 1 1 5728CC2C
P 1550 1850
F 0 "L6" V 1500 1850 40  0000 C CNN
F 1 "74279204" V 1650 1850 40  0000 C CNN
F 2 "Capacitors_SMD:C_0805" H 1550 1850 60  0001 C CNN
F 3 "~" H 1550 1850 60  0000 C CNN
	1    1550 1850
	0    1    1    0   
$EndComp
Connection ~ 1950 1850
Wire Wire Line
	1250 1850 1100 1850
Wire Wire Line
	2750 3600 1950 3600
Connection ~ 1950 3600
$Comp
L C-RESCUE-modballoon C20
U 1 1 5728CCEE
P 3950 7050
F 0 "C20" H 3950 7150 40  0000 L CNN
F 1 "1M" H 3956 6965 40  0000 L CNN
F 2 "Capacitors_SMD:C_0603" H 3988 6900 30  0001 C CNN
F 3 "~" H 3950 7050 60  0000 C CNN
	1    3950 7050
	1    0    0    -1  
$EndComp
$Comp
L C-RESCUE-modballoon C21
U 1 1 5728CCF4
P 4300 7050
F 0 "C21" H 4300 7150 40  0000 L CNN
F 1 "M1" H 4306 6965 40  0000 L CNN
F 2 "Capacitors_SMD:C_0603" H 4338 6900 30  0001 C CNN
F 3 "~" H 4300 7050 60  0000 C CNN
	1    4300 7050
	1    0    0    -1  
$EndComp
$Comp
L C-RESCUE-modballoon C22
U 1 1 5728CCFA
P 4650 7050
F 0 "C22" H 4650 7150 40  0000 L CNN
F 1 "M1" H 4656 6965 40  0000 L CNN
F 2 "Capacitors_SMD:C_0603" H 4688 6900 30  0001 C CNN
F 3 "~" H 4650 7050 60  0000 C CNN
	1    4650 7050
	1    0    0    -1  
$EndComp
$Comp
L C-RESCUE-modballoon C24
U 1 1 5728CD00
P 5000 7050
F 0 "C24" H 5000 7150 40  0000 L CNN
F 1 "M1" H 5006 6965 40  0000 L CNN
F 2 "Capacitors_SMD:C_0603" H 5038 6900 30  0001 C CNN
F 3 "~" H 5000 7050 60  0000 C CNN
	1    5000 7050
	1    0    0    -1  
$EndComp
$Comp
L GND-RESCUE-modballoon #PWR044
U 1 1 5728CD06
P 3950 7400
F 0 "#PWR044" H 3950 7400 30  0001 C CNN
F 1 "GND" H 3950 7330 30  0001 C CNN
F 2 "" H 3950 7400 60  0000 C CNN
F 3 "" H 3950 7400 60  0000 C CNN
	1    3950 7400
	1    0    0    -1  
$EndComp
$Comp
L GND-RESCUE-modballoon #PWR045
U 1 1 5728CD0C
P 4300 7400
F 0 "#PWR045" H 4300 7400 30  0001 C CNN
F 1 "GND" H 4300 7330 30  0001 C CNN
F 2 "" H 4300 7400 60  0000 C CNN
F 3 "" H 4300 7400 60  0000 C CNN
	1    4300 7400
	1    0    0    -1  
$EndComp
$Comp
L GND-RESCUE-modballoon #PWR046
U 1 1 5728CD12
P 4650 7400
F 0 "#PWR046" H 4650 7400 30  0001 C CNN
F 1 "GND" H 4650 7330 30  0001 C CNN
F 2 "" H 4650 7400 60  0000 C CNN
F 3 "" H 4650 7400 60  0000 C CNN
	1    4650 7400
	1    0    0    -1  
$EndComp
$Comp
L GND-RESCUE-modballoon #PWR047
U 1 1 5728CD22
P 5000 7400
F 0 "#PWR047" H 5000 7400 30  0001 C CNN
F 1 "GND" H 5000 7330 30  0001 C CNN
F 2 "" H 5000 7400 60  0000 C CNN
F 3 "" H 5000 7400 60  0000 C CNN
	1    5000 7400
	1    0    0    -1  
$EndComp
Wire Wire Line
	3950 6850 3950 6700
Connection ~ 3950 6700
Wire Wire Line
	3950 7400 3950 7250
Wire Wire Line
	4300 7400 4300 7250
Wire Wire Line
	4300 6850 4300 6700
Connection ~ 4300 6700
Wire Wire Line
	4650 6850 4650 6700
Connection ~ 4650 6700
Wire Wire Line
	4650 7400 4650 7250
Wire Wire Line
	5000 7400 5000 7250
Wire Wire Line
	5000 6850 5000 6700
Connection ~ 5000 6700
$Comp
L R-RESCUE-modballoon R5
U 1 1 5728D043
P 1650 4100
F 0 "R5" H 1750 4150 40  0000 C CNN
F 1 "4K7" H 1750 4050 40  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 1580 4100 30  0001 C CNN
F 3 "~" H 1650 4100 30  0000 C CNN
	1    1650 4100
	1    0    0    -1  
$EndComp
$Comp
L GND-RESCUE-modballoon #PWR048
U 1 1 5728D089
P 1650 4450
F 0 "#PWR048" H 1650 4450 30  0001 C CNN
F 1 "GND" H 1650 4380 30  0001 C CNN
F 2 "" H 1650 4450 60  0000 C CNN
F 3 "" H 1650 4450 60  0000 C CNN
	1    1650 4450
	1    0    0    -1  
$EndComp
Wire Wire Line
	1650 4450 1650 4350
$Comp
L R-RESCUE-modballoon R4
U 1 1 5728D0ED
P 1650 3400
F 0 "R4" H 1750 3450 40  0000 C CNN
F 1 "22K" H 1750 3350 40  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 1580 3400 30  0001 C CNN
F 3 "~" H 1650 3400 30  0000 C CNN
	1    1650 3400
	1    0    0    -1  
$EndComp
Wire Wire Line
	1650 3050 1650 3150
Wire Wire Line
	2750 3800 1650 3800
Wire Wire Line
	1650 3650 1650 3850
Connection ~ 1650 3800
Wire Wire Line
	1100 3050 1650 3050
$Comp
L FA-238V-12MHz X1
U 1 1 5728D240
P 4100 900
AR Path="/5728D240" Ref="X1"  Part="1" 
AR Path="/5727590C/5728D240" Ref="X1"  Part="1" 
F 0 "X1" H 3950 1000 60  0000 C CNN
F 1 "FA-238V-12MHZ" H 4100 900 60  0000 C CNN
F 2 "Balloln_pretty:crystal_FA238-TSX3225" H 4100 900 60  0001 C CNN
F 3 "" H 4100 900 60  0000 C CNN
	1    4100 900 
	1    0    0    -1  
$EndComp
Wire Wire Line
	3600 1050 3600 2850
Wire Wire Line
	3350 1050 3750 1050
Wire Wire Line
	4450 1150 4850 1150
Wire Wire Line
	4600 1150 4600 1350
Wire Wire Line
	4600 1350 3700 1350
Wire Wire Line
	3700 1350 3700 2850
$Comp
L C-RESCUE-modballoon C23
U 1 1 5728D362
P 4850 1350
F 0 "C23" H 4850 1450 40  0000 L CNN
F 1 "18" H 4856 1265 40  0000 L CNN
F 2 "Capacitors_SMD:C_0603" H 4888 1200 30  0001 C CNN
F 3 "~" H 4850 1350 60  0000 C CNN
	1    4850 1350
	1    0    0    -1  
$EndComp
$Comp
L C-RESCUE-modballoon C19
U 1 1 5728D37B
P 3350 1350
F 0 "C19" H 3350 1450 40  0000 L CNN
F 1 "18" H 3356 1265 40  0000 L CNN
F 2 "Capacitors_SMD:C_0603" H 3388 1200 30  0001 C CNN
F 3 "~" H 3350 1350 60  0000 C CNN
	1    3350 1350
	1    0    0    -1  
$EndComp
Connection ~ 3600 1050
Connection ~ 4600 1150
$Comp
L GND-RESCUE-modballoon #PWR049
U 1 1 5728D4A8
P 4850 1700
F 0 "#PWR049" H 4850 1700 30  0001 C CNN
F 1 "GND" H 4850 1630 30  0001 C CNN
F 2 "" H 4850 1700 60  0000 C CNN
F 3 "" H 4850 1700 60  0000 C CNN
	1    4850 1700
	1    0    0    -1  
$EndComp
$Comp
L GND-RESCUE-modballoon #PWR050
U 1 1 5728D4B7
P 3350 1700
F 0 "#PWR050" H 3350 1700 30  0001 C CNN
F 1 "GND" H 3350 1630 30  0001 C CNN
F 2 "" H 3350 1700 60  0000 C CNN
F 3 "" H 3350 1700 60  0000 C CNN
	1    3350 1700
	1    0    0    -1  
$EndComp
Wire Wire Line
	3350 1550 3350 1700
$Comp
L SAM_JTAG K8
U 1 1 5728D57D
P 8100 2550
F 0 "K8" H 7950 2650 60  0000 C CNN
F 1 "SAM_JTAG" H 8100 2550 60  0000 C CNN
F 2 "Pin_Headers:Pin_Header_Straight_2x10" H 8100 2550 60  0001 C CNN
F 3 "~" H 8100 2550 60  0000 C CNN
	1    8100 2550
	1    0    0    -1  
$EndComp
Wire Wire Line
	8650 1850 8650 2650
Wire Wire Line
	8650 2650 8600 2650
Connection ~ 4000 1850
Wire Wire Line
	4850 1700 4850 1550
Wire Wire Line
	3350 1150 3350 1050
$Comp
L GND-RESCUE-modballoon #PWR051
U 1 1 5728D847
P 8650 3650
F 0 "#PWR051" H 8650 3650 30  0001 C CNN
F 1 "GND" H 8650 3580 30  0001 C CNN
F 2 "" H 8650 3650 60  0000 C CNN
F 3 "" H 8650 3650 60  0000 C CNN
	1    8650 3650
	1    0    0    -1  
$EndComp
Wire Wire Line
	8600 2750 8650 2750
Wire Wire Line
	8650 2750 8650 3650
Wire Wire Line
	8600 2850 8650 2850
Connection ~ 8650 2850
Wire Wire Line
	8600 2950 8650 2950
Connection ~ 8650 2950
Wire Wire Line
	8600 3050 8650 3050
Connection ~ 8650 3050
Wire Wire Line
	8600 3150 8650 3150
Connection ~ 8650 3150
Wire Wire Line
	8600 3250 8650 3250
Connection ~ 8650 3250
Wire Wire Line
	8600 3350 8650 3350
Connection ~ 8650 3350
Wire Wire Line
	8600 3450 8650 3450
Connection ~ 8650 3450
Wire Wire Line
	8600 3550 8650 3550
Connection ~ 8650 3550
Wire Wire Line
	7550 2650 7650 2650
Wire Wire Line
	7550 1850 7550 2650
Connection ~ 7550 1850
$Comp
L R-RESCUE-modballoon R10
U 1 1 5728DD70
P 7250 2250
F 0 "R10" H 7350 2300 40  0000 C CNN
F 1 "100K" H 7400 2200 40  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 7180 2250 30  0001 C CNN
F 3 "~" H 7250 2250 30  0000 C CNN
	1    7250 2250
	1    0    0    -1  
$EndComp
Wire Wire Line
	7250 2000 7250 1850
Connection ~ 7250 1850
Wire Wire Line
	7650 2750 7250 2750
Wire Wire Line
	7250 2750 7250 2500
$Comp
L R-RESCUE-modballoon R9
U 1 1 5728DE73
P 6950 2250
F 0 "R9" H 7050 2300 40  0000 C CNN
F 1 "100K" H 7100 2200 40  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 6880 2250 30  0001 C CNN
F 3 "~" H 6950 2250 30  0000 C CNN
	1    6950 2250
	1    0    0    -1  
$EndComp
$Comp
L R-RESCUE-modballoon R8
U 1 1 5728DE79
P 6650 2250
F 0 "R8" H 6750 2300 40  0000 C CNN
F 1 "100K" H 6800 2200 40  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 6580 2250 30  0001 C CNN
F 3 "~" H 6650 2250 30  0000 C CNN
	1    6650 2250
	1    0    0    -1  
$EndComp
$Comp
L R-RESCUE-modballoon R7
U 1 1 5728DE7F
P 6350 2250
F 0 "R7" H 6450 2300 40  0000 C CNN
F 1 "100K" H 6500 2200 40  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 6280 2250 30  0001 C CNN
F 3 "~" H 6350 2250 30  0000 C CNN
	1    6350 2250
	1    0    0    -1  
$EndComp
$Comp
L R-RESCUE-modballoon R6
U 1 1 5728DE85
P 6050 2250
F 0 "R6" H 6150 2300 40  0000 C CNN
F 1 "100K" H 6200 2200 40  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 5980 2250 30  0001 C CNN
F 3 "~" H 6050 2250 30  0000 C CNN
	1    6050 2250
	1    0    0    -1  
$EndComp
Wire Wire Line
	6950 2000 6950 1850
Connection ~ 6950 1850
Wire Wire Line
	6650 2000 6650 1850
Connection ~ 6650 1850
Wire Wire Line
	6350 2000 6350 1850
Connection ~ 6350 1850
Wire Wire Line
	6050 2000 6050 1850
Connection ~ 6050 1850
Wire Wire Line
	7650 2850 6950 2850
Wire Wire Line
	6950 2500 6950 5100
Wire Wire Line
	6950 5100 5600 5100
Connection ~ 6950 2850
Wire Wire Line
	5800 2950 7650 2950
Wire Wire Line
	6650 2950 6650 2500
Wire Wire Line
	5800 2950 5800 2350
Wire Wire Line
	5800 2350 4700 2350
Wire Wire Line
	4700 2350 4700 2850
Connection ~ 6650 2950
Wire Wire Line
	5700 3050 7650 3050
Wire Wire Line
	6350 3050 6350 2500
Wire Wire Line
	7650 3150 7500 3150
Wire Wire Line
	7500 3150 7500 3050
Connection ~ 7500 3050
Wire Wire Line
	5700 3050 5700 2250
Wire Wire Line
	5700 2250 4500 2250
Wire Wire Line
	4500 2250 4500 2850
Connection ~ 6350 3050
Wire Wire Line
	7650 3250 5600 3250
Wire Wire Line
	5600 3250 5600 2500
Wire Wire Line
	5600 2500 4900 2500
Wire Wire Line
	4900 2500 4900 2850
Wire Wire Line
	5600 4500 7200 4500
Wire Wire Line
	7200 4500 7200 3350
Wire Wire Line
	6050 3350 7650 3350
Wire Wire Line
	6050 2500 6050 3350
Connection ~ 7200 3350
$EndSCHEMATC
