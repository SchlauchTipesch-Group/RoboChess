#include "SteppersControl.h"

// 7V | 10V
SteppersControl controller;
int i = 0;

void setup()
{
  // Constructor
  Stepper* xStepper = new Stepper(200, 6, 8, 7, 9);
  Stepper* yStepper = new Stepper(200, 2, 4, 3, 5);
  controller = SteppersControl(xStepper, yStepper);
}

void loop()
{
  controller.manualControl();
}
