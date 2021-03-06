/*
  CosmicWatch Desktop Muon Detector Arduino Code

  This code does not use the microSD card reader/writer, but does used the OLED screen.
  
  Questions?
  Spencer N. Axani
  saxani@mit.edu

  Requirements: Sketch->Include->Manage Libraries:
  SPI, EEPROM, SD, and Wire are probably already installed.
  1. Adafruit SSD1306     -- by Adafruit Version 1.0.1
  2. Adafruit GFX Library -- by Adafruit Version 1.0.2
  3. TimerOne             -- by Jesse Tane et al. Version 1.1.0
*/

#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
#include <TimerOne.h>
#include <Wire.h>
#include <SPI.h>
#include <EEPROM.h>



const int SIGNAL_THRESHOLD      = 50;    // Min threshold to trigger on. See calibration.pdf for conversion to mV.
const int RESET_THRESHOLD       = 15;    

const int cal_max = 1023;

//INTERUPT SETUP
#define TIMER_INTERVAL 1000000          // Every 1,000,000 us the timer will update the OLED readout

//OLED SETUP
#define OLED_RESET 10
Adafruit_SSD1306 display(OLED_RESET);

//initialize variables
char detector_name[40];

unsigned long time_stamp                      = 0L;
unsigned long measurement_deadtime            = 0L;
unsigned long time_measurement                = 0L;      // Time stamp
unsigned long interrupt_timer                 = 0L;      // Time stamp
int start_time                                = 0L;      // Reference time for all the time measurements
unsigned long total_deadtime                  = 0L;      // total measured deadtime
unsigned long waiting_t1                      = 0L;
unsigned long measurement_t1;
unsigned long measurement_t2;

float sipm_voltage                            = 0;
long int count                                = 0L;      // A tally of the number of muon counts observed
float last_sipm_voltage                       = 0;
float temperatureC;

byte waiting_for_interupt                     = 0;
byte SLAVE;
byte MASTER;
byte keep_pulse                               = 0;

void setup() {
  analogReference (EXTERNAL);
  ADCSRA &= ~(bit (ADPS0) | bit (ADPS1) | bit (ADPS2));  // clear prescaler bits
  ADCSRA |= bit (ADPS0) | bit (ADPS1);                   // Set prescaler to 8
  Serial.begin(9600);

  pinMode(3, OUTPUT);
  pinMode(6, INPUT);
  if (digitalRead(6) == HIGH) {
      SLAVE = 1;
      MASTER = 0;
      digitalWrite(3,HIGH);
      delay(1000);}

  else{
      delay(10);
      MASTER = 1;
      SLAVE = 0;
      pinMode(6, OUTPUT);
      digitalWrite(6, HIGH);}

  digitalWrite(3,LOW);
  if (MASTER == 1) {digitalWrite(6, LOW);}
  
  Serial.println("# Calibration raw adc with signal threshold " + (String)SIGNAL_THRESHOLD);
  
  
}

void loop()
{
  while (1){
    if (analogRead(A0) > SIGNAL_THRESHOLD){ 

      // Make a measurement of the pulse amplitude
      int adc = analogRead(A0);
      
      Serial.println(adc);
      delay(100);
}}}
