#include "main.h"


#define LED       PIN_C0  
#define SS        PIN_D1
#define ARESET    PIN_D2
#define CONV      PIN_D0
#define POWER_SW  PIN_D3 

void main()
{
   int16 counter;
   
   setup_adc_ports(NO_ANALOGS);
   setup_adc(ADC_CLOCK_DIV_2);
   setup_psp(PSP_DISABLED);
   setup_spi(SPI_SS_DISABLED);
   setup_timer_0(RTCC_INTERNAL|RTCC_DIV_1);
   setup_timer_1(T1_DISABLED);
   setup_timer_2(T2_DISABLED,0,1);
   setup_comparator(NC_NC_NC_NC);
   setup_vref(FALSE);

   while(true)
   {
      while ( input(SS) )  // waits for SS to go low
      {
         //TODO watchdog
      }
      output_high(ARESET);
      delay_us(10);
      output_low(ARESET);
      delay_us(60);
      output_high(CONV);
      delay_us(4);
      output_low(CONV);
      
      counter++;
      
      //!!! TODO LED proti zemi.
      if (counter==10000) output_high(LED);
      if (counter==11000) {output_low(LED); counter=0;}
      restart_wdt();
   }
}
