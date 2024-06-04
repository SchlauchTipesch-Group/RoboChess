#include "SteppersControl.h"
#include "Stepper.h"

SteppersControl::SteppersControl() : _xStepper(200, 6, 8, 7, 9), _yStepper(200, 2, 4, 3, 5)
{
  _xStepper.setSpeed(100);
  _yStepper.setSpeed(150);

  pinMode(10, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT_PULLUP);

  //calibrateAxes();
}

void SteppersControl::calibrateX()
{
  while (digitalRead(10))
  {
    _xStepper.step(-1);
  }  
}
void SteppersControl::calibrateY()
{
  // Calibrate Y axis
  while (digitalRead(11))
  {
    _yStepper.step(1);
  }
}
void SteppersControl::calibrateAxes()
{
  this->calibrateX();
  this->calibrateY();
}

void SteppersControl::manualControl()
{
  int xDirection = analogRead(A0);
  int yDirection = analogRead(A1);

  if (xDirection > 550)
  {
    _xStepper.step(1);
    _xAxisLocation++;
  }
  else if (xDirection < 450)
  {
    _xStepper.step(-1);
    _xAxisLocation--;
  }
  if (yDirection > 550)
  {
    _yStepper.step(1);
    _yAxisLocation++;
  }
  else if (yDirection < 450)
  {
    _yStepper.step(-1);
    _yAxisLocation--;
  }
  if (!digitalRead(A2))
  {
    calibrateAxes();
  }
}

void SteppersControl::move(const char xDistance, const char yDistance)
{
  // Move axes
  int x = xDistance * 34 * 2;
  int y = -yDistance * 34 * 6;

  Serial.print("X: ");
  Serial.println(x, DEC);

  Serial.print("Y: ");
  Serial.println(y, DEC);

  _xStepper.step(x);
  Serial.println("Done");
  _yStepper.step(y);

  // Update the current location of each axis
  _xAxisLocation += x;
  _yAxisLocation += y;
}