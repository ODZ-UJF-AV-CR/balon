#include "main.h"


#define LED       PIN_C0  
#define SS        PIN_D1
#define ARESET    PIN_D2
#define CONV      PIN_D0
#define POWER_SW  PIN_D3 

#define RELE_ON   PIN_C6
#define RELE_OFF  PIN_C5

#define DEATHTIME 1  // not response time in minutes

void main()
{
   int16 led_counter;
   int32 watchdog_counter;
   
   setup_adc_ports(NO_ANALOGS);
   setup_adc(ADC_CLOCK_DIV_2);
   setup_psp(PSP_DISABLED);
   setup_spi(SPI_SS_DISABLED);
   setup_timer_0(RTCC_INTERNAL|RTCC_DIV_1);
   setup_timer_1(T1_DISABLED);
   setup_timer_2(T2_DISABLED,0,1);
   setup_comparator(NC_NC_NC_NC);
   setup_vref(FALSE);
   
   output_low(RELE_OFF);
   output_high(RELE_ON);
   delay_ms(500);
   output_low(RELE_ON);

   while(true)
   {
      watchdog_counter = 0;
      while ( input(SS) )  // waits for SS to go low
      {
         //TODO watchdog
         restart_wdt();
         watchdog_counter++;
         if (watchdog_counter > 212765 * 60 * DEATHTIME)
         {
            output_high(RELE_OFF);
            delay_ms(500);
            output_low(RELE_OFF);
            delay_ms(5000);
            reset_cpu();
         }
      }
      output_high(ARESET);
      delay_us(10);
      output_low(ARESET);
      delay_us(60);
      output_high(CONV);
      delay_us(4);
      output_low(CONV);
      
      led_counter++;
      
      //!!! TODO LED proti zemi.
      if (led_counter==10000) output_high(LED);
      if (led_counter==11000) {output_low(LED); led_counter=0;}
      restart_wdt();
   }
}
