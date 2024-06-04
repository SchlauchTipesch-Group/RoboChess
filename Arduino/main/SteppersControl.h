// Includes and Definitions
#include <Arduino.h>
#include "Stepper.h"

// X Diameter 40mm
// Y Diameter 12mm

class SteppersControl
{
public:
    SteppersControl();
    void move(const char xDistance, const char yDistance);
    void manualControl();
private:
    void calibrateAxes();
    void calibrateX();
    void calibrateY();

private:
    Stepper _xStepper;
    Stepper _yStepper;
    int _xAxisLocation;
    int _yAxisLocation;
    int _currentSquare;
};