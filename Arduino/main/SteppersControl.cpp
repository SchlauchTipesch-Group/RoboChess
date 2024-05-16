#include "Arduino.h"
#include "SteppersControl.h"
#include "Stepper.h"

SteppersControl::SteppersControl(Stepper* xStepper, Stepper* yStepper)
{
  _xStepper = xStepper;
  _yStepper = yStepper;
  pinMode(10, INPUT_PULLUP);
  pinMode(11, INPUT_PULLUP);
  pinMode(A0, INPUT);
  pinMode(A1, INPUT);
  pinMode(A2, INPUT_PULLUP);

  Serial.begin(115200);
  
  (*_xStepper).setSpeed(75);
  (*_yStepper).setSpeed(150);
}
SteppersControl::SteppersControl()
{
}

SteppersControl::~SteppersControl()
{
  delete _xStepper;
  delete _yStepper;
}



void SteppersControl::calibrateX()
{
  while (digitalRead(10))
  {
    (*_xStepper).step(1);
  }  
}
void SteppersControl::calibrateY()
{
  // Calibrate Y axis
  while (digitalRead(11))
  {
    (*_yStepper).step(1);
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
    _xStepper->step(1);
    _xAxisLocation++;
  }
  else if (xDirection < 450)
  {
    _xStepper->step(-1);
    _xAxisLocation--;
  }
  if (yDirection > 550)
  {
    _yStepper->step(1);
    _yAxisLocation++;
  }
  else if (yDirection < 450)
  {
    _yStepper->step(-1);
    _yAxisLocation--;
  }
  if (!digitalRead(A2))
  {
    calibrateAxes();
  }
}

void SteppersControl::goToSquare(int targetSquare)
{
  targetSquare = targetSquare % 64;
  int targetCol =  targetSquare / 8;
  int targetRow =  targetSquare % 8;
  int stepCol = 50;
  int stepRow = 50;
  int currCol = (this->_currentSquare / 8);
  int currRow = (this->_currentSquare / 8);

  targetCol = targetCol - currCol;
  targetRow = targetRow - currRow;

  if(targetCol < 0)
  {
    targetCol = targetCol * (-1);
    stepCol = -50;
  }
  if(targetRow < 0)
  {
    targetRow= targetRow * (-1);
    stepRow = -50;
  }

  currCol = 0;
  currRow = 0;
  for (int i = 0; i < 8; i++)
  {
    if (currCol < targetCol)
    {
      (*_yStepper).step(stepCol);
      currCol++;
      delay(50);
    }
    
    if (currRow < targetRow)
    {
      (*_xStepper).step(stepRow);
      currRow++;
      delay(100);
    }
  }
}

// Copy assignment operator
SteppersControl& SteppersControl::operator=(const SteppersControl& other)
{
    if (this!= &other)
    {
        delete _xStepper;
        delete _yStepper;

        // Assign new Stepper objects
        _xStepper = (other._xStepper);
        _yStepper = (other._yStepper);

        // Copy other member variables
        //stepsPerRev = other.stepsPerRev;
        _xAxisLocation = other._xAxisLocation;
        _yAxisLocation = other._yAxisLocation;
        _currentSquare = other._currentSquare;
    }
    return *this;
}