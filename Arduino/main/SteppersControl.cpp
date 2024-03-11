#include "Arduino.h"
#include "SteppersControl.h"

SteppersControl::SteppersControl(const STEP_PINS xAxisStepPin, const DIR_PINS xAxisDirPin, const STEP_PINS yAxisStepPin, const DIR_PINS yAxisDirPin)
{
  _xAxisStepPin = xAxisStepPin;
  _xAxisDirPin = xAxisDirPin;
  _yAxisStepPin = yAxisStepPin;
  _yAxisDirPin = yAxisDirPin;

  // TODO: Add calibration function
  _xAxisLocation = 0;
  _yAxisLocation = 0;
  _currentSquare = 0;

  // Turn on the enable pin
  pinMode(EN_PIN, OUTPUT);
 	digitalWrite(EN_PIN, HIGH);

 	pinMode(_xAxisStepPin, OUTPUT);
 	pinMode(_xAxisDirPin, OUTPUT);
  pinMode(_yAxisStepPin, OUTPUT);
 	pinMode(_yAxisDirPin, OUTPUT);
}

void SteppersControl::goToSquare(const int targetSquare)
{
  int targetRow = targetSquare % 8;
  int targetCol = targetSquare / 8;

  move(targetRow > _currentSquare % 8,
    targetRow * SQUARE_SIZE,
    targetCol > _currentSquare / 8,
    targetCol * SQUARE_SIZE
  );

  _currentSquare = targetSquare;
}

void SteppersControl::move(const bool xAxisDirection, const int xAxisDistance, const bool yAxisDirection, const int yAxisDistance)
{
  // Declaring the direction for each axis
  digitalWrite(_xAxisDirPin, xAxisDirection);
  digitalWrite(_yAxisDirPin, yAxisDirection);

  // Run until both axes move their target distance
  for (int i = 0; (i < X_STEPS_PER_MM * xDistance) || (i < Y_STEPS_PER_MM * yDistance); i++)
  {
    // If the X axis has more to go, set step pin to HIGH
    if (i < X_STEPS_PER_MM * xDistance)
    {
      digitalWrite(_xAxisStepPin, HIGH);
    }
    // Else, set step pin to LOW so that it wouldn't interfere with the other axis
    else
    {
      digitalWrite(_xAxisStepPin, LOW);
    }
    
    // If the Y axis has more to go, set step pin to HIGH
    if (i < Y_STEPS_PER_MM * yDistance)
    {
      digitalWrite(_yAxisStepPin, HIGH);
    }
    // Else, set step pin to LOW so that it wouldn't interfere with the other axis
    else
    {
      digitalWrite(_yAxisStepPin, LOW);
    }

    // Delay and set both step pins to LOW
    delay(5);
    digitalWrite(_xAxisStepPin, LOW);
    digitalWrite(_yAxisStepPin, LOW);
    delay(5);
  }

  // Update the current location of each axis
  _xAxisLocation += xAxisDistance;
  _yAxisLocation += yAxisDistance;
}
