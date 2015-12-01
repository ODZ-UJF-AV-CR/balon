//GPS modul
//RXD - PD1
//TXD - PD0

//SDcard
//DAT3 - PD4
//CMD - PB3
//CLK - PB5
//DAT0 - PB4
//detect - PB4

 //USB232 - ATMEGA328P
 //DRT-boot
 //TXD-RX
 //RXD-TX



#include <SoftwareSerial.h>
#include <SD.h>
#include  <math.h>
#include  <stdlib.h>



SoftwareSerial so1Serial(5, 6); //pro pripojeni modulu GPS (PD5 PD6) rx tx
char filename[10]; //pro ulozeni naszvu souboru
char dataUvodni[60];
int c=0; //pro ohlidani aby se nezapisovala hlavicka souboru vicekrat
int b=0; //pro ohlidani aby se pokazde nevytvarel nový soubor
int a=0; //promena pro cislo souboru
File myFile;



void setup()
  {
  int count=0;
  //so1Serial.begin(9600);
  Serial.begin(9600);
  pinMode(10, OUTPUT); //sd karta
  if (!SD.begin(4)) {    //inicializace SD karty
    //Serial.println("inicializace se nepovedla");
    return;
    }
  //Serial.println("inicializace provedena"); 
 
 //vytvori nazev souboru
 if(b==0) //vyhledani jmena pro soubor, po kazdem zapnuti se vytvori novy soubor
      {
      sprintf(filename, "data%d.txt",a);
      while(SD.exists(filename)==1)
      {
      a=a+1;
      sprintf(filename, "data%d.txt",a);
      }
      b=1;
      }
    else
      {
      } 
 
//otevre, nebo vytvory soubor
//s nazvem v promenné filename
File myFile = SD.open(filename, FILE_WRITE);

if (myFile) 
  {
    if(c==0) //obsahuje hlavicku souboru
      {
      myFile.print("Dataloger balon 2015 \n");
      delay(10);
      myFile.print(" \n");
     // Serial.print(dataUvodni);
      c=1;
      }
    else
      {
      } 
    
  
     
    // uzavreni souboru
    myFile.close();
    
  }
else
  {
  //pri neotevreni souboru
  //Serial.println("Nepodarilo se otevrit soubor");
  }



 
 }



void loop () //nekonecna smycka
  {
     

//otevre, nebo vytvory soubor
//s nazvem v promenné filename
File myFile = SD.open(filename, FILE_WRITE);

if (myFile) 
  {
   
    //cekani na data ze seriove linky
    while(Serial.available()==0)
      {
      }

    delay(30);
  

    //vycet dat ze seriove linky
    while (Serial.available())
      {
      char GPSdata = Serial.read();
      myFile.print(GPSdata);
      //Serial.print(GPSdata);
      }
    
    
 
    // uzavreni souboru
    myFile.close();

  }
else
  {
  //pri neotevreni souboru
  //Serial.println("Nepodarilo se otevrit soubor");
  }

}






















