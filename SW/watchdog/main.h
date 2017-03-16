#include <16F887.h>
#device adc=8

#FUSES WDT                      //Watch Dog Timer
#FUSES HS //INTRC_IO                 //Internal RC Osc, no CLKOUT
#FUSES PUT                      //Power Up Timer
#FUSES MCLR //NOMCLR                   //Master Clear pin used for I/O
#FUSES NOPROTECT                //Code not protected from reading
#FUSES NOCPD                    //No EE protection
#FUSES BROWNOUT                 //Reset when brownout detected
#FUSES NOIESO                     //Internal External Switch Over mode enabled
#FUSES NOFCMEN                    //Fail-safe clock monitor enabled
#FUSES NOLVP                    //No low voltage prgming, B3(PIC16) or B5(PIC18) used for I/O
#FUSES NODEBUG                  //No Debug mode for ICD
#FUSES NOWRT                    //Program memory not write protected
#FUSES BORV21                   //Brownout reset at 2.1V

#use delay(clock=20000000,RESTART_WDT)
#use rs232(UART1,baud=9600,ERRORS,RESTART_WDT)
//#pragma use rs232(baud=9600, xmit=PIN_C6, rcv=PIN_C7)

