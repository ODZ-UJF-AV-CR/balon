/*
  CANDY based on Mighty 1284p
 
SDcard
------
DAT3 SS 4 B4
CMD MOSI 5 B5
DAT0 MISO 6 B6
CLK SCK 7 B7

The following needs to be added to the line mentioning the atmega644 in
/usr/share/arduino/libraries/SD/utility/Sd2PinMap.h:

    || defined(__AVR_ATmega1284P__)

so that it reads:

    #elif defined(__AVR_ATmega644P__) || defined(__AVR_ATmega644__)|| defined(__AVR_ATmega1284P__)
    
 
*/

#include <SD.h>
#include "wiring_private.h"
#include <SoftwareSerial.h>

SoftwareSerial mySerial(18, 19); // RX, TX


const int chipSelect = 4;
int RESET = 0;
uint16_t count = 0;


void setup()
{
 // Open serial communications and wait for port to open:
  Serial.begin(9600);
   while (!Serial) 
   {
    ; // wait for serial port to connect. Needed for Leonardo only
   }

  mySerial.begin(9600);
  //mySerial.println("#Cvak...");

  Serial.print("#Initializing SD card...");
  // make sure that the default chip select pin is set to
  // output, even if you don't use it:
  pinMode(10, OUTPUT);
  
  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) 
  {
    Serial.println("#Card failed, or not present");
    // don't do anything more:
    return;
  }
  Serial.println("#card initialized.");
  
// Read Analog Differential without gain (read datashet of ATMega1280 and ATMega2560 for refference)
// Use analogReadDiff(NUM)
// NUM	|	POS PIN		|	NEG PIN		| 	GAIN
//	0	|	A0			|	A1			|	1x
//	1	|	A1			|	A1			|	1x
//	2	|	A2			|	A1			|	1x
//	3	|	A3			|	A1			|	1x
//	4	|	A4			|	A1			|	1x
//	5	|	A5			|	A1			|	1x
//	6	|	A6			|	A1			|	1x
//	7	|	A7			|	A1			|	1x
//	8	|	A8			|	A9			|	1x
//	9	|	A9			|	A9			|	1x
//	10	|	A10			|	A9			|	1x
//	11	|	A11			|	A9			|	1x
//	12	|	A12			|	A9			|	1x
//	13	|	A13			|	A9			|	1x
//	14	|	A14			|	A9			|	1x
//	15	|	A15			|	A9			|	1x
  #define pin 0
  uint8_t analog_reference = INTERNAL1V1; // DEFAULT, INTERNAL, INTERNAL1V1, INTERNAL2V56, or EXTERNAL

  ADMUX = (analog_reference << 6) | ((pin | 0x10) & 0x1F);

  pinMode(RESET, OUTPUT);     
}

int oldValue = 0;  // Variable for filtering death time double detection

void loop()
{
  uint8_t low, high;
  int sensor;
  uint16_t buffer[1024];
  
  for(int n=0; n<1024; n++)
  {
    buffer[n]=0;
  }
  
  digitalWrite(RESET, HIGH);   // Reset peak detector
  digitalWrite(RESET, HIGH);   // Reset peak detector
  digitalWrite(RESET, HIGH);   // Reset peak detector
  digitalWrite(RESET, HIGH);   // Reset peak detector
  digitalWrite(RESET, HIGH);   // Reset peak detector
  digitalWrite(RESET, LOW); 
  for(int n=0; n<10000; n++)
  {
    // start the conversion
    sbi(ADCSRA, ADSC);
    // ADSC is cleared when the conversion finishes
    while (bit_is_set(ADCSRA, ADSC));
    digitalWrite(RESET, HIGH);   // Reset peak detector
    digitalWrite(RESET, LOW); 
   
    
    // we have to read ADCL first; doing so locks both ADCL
    // and ADCH until ADCH is read.  reading ADCL second would
    // cause the results of each conversion to be discarded,
    // as ADCL and ADCH would be locked when it completed.
    low  = ADCL;
    high = ADCH;
    
    // combine the two bytes
    sensor = (high << 8) | low;
  
    // arrange integer value (read ATMega 2560 Datashet p.288) figure 26-15
    if (sensor > 511 )
    {
      sensor -= 1023 ;
    }
    sensor +=30; // Add offset to ground
    if ((sensor>=0)&&(buffer[sensor]<65535)&&(oldValue<sensor)) buffer[sensor]++;
    oldValue = sensor;
    for (int i=0; i<100; i++) {digitalWrite(RESET, LOW);}
  }
  //!!!digitalWrite(RESET, HIGH);   // Reset peak detector
  
  // make a string for assembling the data to log:
  String dataString = "";
  String toModem = "";

  dataString += String(count); 
  dataString += ",";

  for(int n=0; n<(511+31); n++)
  {
    dataString += String(buffer[n]); 
    dataString += ",";
  }

  int noise = 0;
//!!!  for(int n=0; n<(511+31); n++)
  for(int n=2; n<(511+31); n++)
  {
    if(buffer[n]==0)
    {
      noise = n;
      break;
    }
  }
  
  int flux=0;
  for(int n=noise; n<(511+31); n++)
  {
    flux += buffer[n];
  }

  
  toModem = "$CANDY,"+ String(count++) + "," + String(noise) + "," + String(flux) + "*";
/*
  byte checksum = 0
  for(int n=1; n<(length(toModem)-1); n++)
  {
    checksum ^= ord(toModem[n]);
  }
  toModem += hex(checksum);
*/
  
  mySerial.println(toModem);
  dataString += String(noise) + "," + String(flux);

  // open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  File dataFile = SD.open("datalog.txt", FILE_WRITE);

  // if the file is available, write to it:
  if (dataFile) 
  {
    dataFile.println(dataString);  // write to SDcard
    Serial.println(dataString);    // print to terminal
    dataFile.close();
  }  
  // if the file isn't open, pop up an error:
  else 
  {
    Serial.println("#error opening datalog.txt");
  }
}









