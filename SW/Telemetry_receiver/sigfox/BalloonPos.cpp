// BalloonPos.cpp : Defines the entry point for the console application.
//

//#include "stdafx.h"
#include "stdio.h"

int trchar(char v) {
    if (v >= '0' && v <= '9') {
        return v - '0';
    }
    if (v >= 'a' && v <= 'f') {
        return 10 + v - 'a';
    }
    return 0;
}

int main()
{

    size_t bufsize = 100;
    char sigfoxmsg[100];
    char *b = sigfoxmsg;
    int i = 2;
    long latd, lond;
    float lat, lon;
    int h, tmcu, vaccu;
    size_t characters;

    while (1) {
        printf("\n\r Zadej SigFox Zpravu. Bude-li prvni znak K konec programu: ");
        characters = getline(&b,&bufsize,stdin);
        //scanf("%1s", sigfoxmsg);
        if (sigfoxmsg[0] == 'K'){
            printf("Konec Programu");
            break;
        }
        printf("%s\n\r", sigfoxmsg);
         
        latd     = 16 * (16 * (16 * (16 * (16 * trchar(sigfoxmsg[0]) + trchar(sigfoxmsg[1])) + trchar(sigfoxmsg[2])) + trchar(sigfoxmsg[3])) + trchar(sigfoxmsg[4])) + trchar(sigfoxmsg[5]);
        lond     = 16 * (16 * (16 * (16 * (16 * trchar(sigfoxmsg[6]) + trchar(sigfoxmsg[7])) + trchar(sigfoxmsg[8])) + trchar(sigfoxmsg[9])) + trchar(sigfoxmsg[10])) + trchar(sigfoxmsg[11]);
        h         = 16*(16*(16*trchar(sigfoxmsg[12]) + trchar(sigfoxmsg[13])) + trchar(sigfoxmsg[14])) + trchar(sigfoxmsg[15]);
        tmcu     = 16 * (16 * (16 * trchar(sigfoxmsg[16]) + trchar(sigfoxmsg[17])) + trchar(sigfoxmsg[18])) + trchar(sigfoxmsg[19]);
        vaccu     = 16 * (16 * (16 * trchar(sigfoxmsg[20]) + trchar(sigfoxmsg[21])) + trchar(sigfoxmsg[22])) + trchar(sigfoxmsg[23]);

        lat = latd * 360.0 / (float)0x01000000;

        lon = lond * 360.0 / (float)0x01000000;



        printf("Lon: %f %d Lat %f %d \n\r", lat, latd, lon, lond);
        printf("Lon: %f Lat %f Elev %d tmcu %fdeg Vaccu %f V\n\r", lat, lon, h, 0.171417*((float)tmcu) - 279.38, 5.681*3.3 / 4096.00*(float)vaccu);

        printf("%f, %f\n\r", lat, lon);
    }
   
    return 0;
}

