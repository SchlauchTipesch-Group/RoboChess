#include <Wire.h>
#include "SteppersControl.h"

#define SLAVE_ADDR 0x08

SteppersControl controller;
char buffer[32];
bool bufferEmpty = true;

void setup() {
  Serial.begin(115200);  // Initialize Serial communication

  controller = SteppersControl();

  Serial.println("Running!");

  Wire.begin(SLAVE_ADDR);  // Initialize I2C as slave
  Wire.onReceive(receiveEvent);  // Register event
}

void loop() {
  if (!bufferEmpty)
  {
    controller.move(buffer[1], buffer[2]);
    bufferEmpty = true;
  }
  delay(100);
}

void receiveEvent(int howMany) {
  int count = 0;
  
  while (Wire.available())
  {
    buffer[count] = Wire.read();
    count++;
  }

  bufferEmpty = false;
}
