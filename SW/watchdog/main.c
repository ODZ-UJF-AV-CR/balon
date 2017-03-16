// WatchDog for Ballon

#include "main.h"


#define LED       PIN_C0  

#define RELE_ON   PIN_D4
#define RELE_OFF  PIN_D5

#define DEATHTIME 1  // not response time in minutes

void main()
{
   int32 watchdog_counter;
   
   setup_wdt(WDT_2304MS);
   setup_adc_ports(NO_ANALOGS);
   setup_adc(ADC_CLOCK_DIV_2);
   //setup_psp(PSP_DISABLED);
   setup_spi(SPI_SS_DISABLED);
   setup_timer_0(RTCC_INTERNAL|RTCC_DIV_1);
   setup_timer_1(T1_DISABLED);
   setup_ccp1(CCP_OFF);
   setup_timer_2(T2_DISABLED,0,1);
   setup_comparator(NC_NC_NC_NC);
   setup_vref(FALSE);
   
   output_low(RELE_OFF);
   output_high(RELE_ON);
   delay_ms(500);
   output_low(RELE_ON);

   watchdog_counter = 0;
   while(true)
   {
      restart_wdt();
      if (kbhit())
      {
         getc();
         output_toggle(LED);
         watchdog_counter = 0;
      }
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
}
