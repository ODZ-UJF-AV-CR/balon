#include "main.h"

#define TX PIN_C0  //To the transmitter

#define  DOT   100
#define  TONE  500   
#define  TONE2 500   
#define  CHARSPACE  800
#define  WORDSPACE  1600

#use fast_io (C)

void b(int xx)   // beep
{
   int16 i;

   if (xx == 1)
   {
      for(i=0; i<(3*DOT); i++)   // dash
      {
         output_high(TX);
         delay_us(TONE2);
         output_low(TX);
         delay_us(TONE2);
      }
   }
   else
   {
      for(i=0; i<DOT; i++)    // dot
      {
         output_high(TX);
         delay_us(TONE);
         output_low(TX);
         delay_us(TONE);
      }
   };
   
   for(i=0; i<DOT; i++)
   {
      output_low(TX);
      delay_us(TONE);
      output_low(TX);
      delay_us(TONE);
   }
   restart_wdt();
}


void main()
{

   setup_adc_ports(NO_ANALOGS|VSS_VDD);
   setup_adc(ADC_CLOCK_DIV_2);
   setup_spi(SPI_SS_DISABLED);
   setup_timer_0(RTCC_INTERNAL|RTCC_DIV_1);
   setup_wdt(WDT_2304MS); //|WDT_DIV_16);
   restart_wdt();
   setup_timer_1(T1_DISABLED);
   setup_timer_2(T2_DISABLED,0,1);
   setup_ccp1(CCP_OFF);
   setup_comparator(NC_NC_NC_NC);// This device COMP currently not supported by the PICWizard
   setup_oscillator(OSC_1MHZ);

   SET_TRIS_C( 0x00 );
   
   while(true)
   {
      b(0);  // l
      b(1);
      b(0);  
      b(0);  
      delay_ms(CHARSPACE);
      b(0);  // e
      delay_ms(CHARSPACE);
      b(1);  // t
      delay_ms(WORDSPACE);
      b(0);  // f
      b(0);  
      b(1);
      b(0);  
      delay_ms(CHARSPACE);
      b(0);  // i
      b(0);  
      delay_ms(CHARSPACE);
      b(1);  // k
      b(0);  
      b(1);      
     
      delay_ms(3000);
   }

}
