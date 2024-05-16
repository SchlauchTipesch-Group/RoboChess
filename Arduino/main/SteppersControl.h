// Includes and Definitions
#include <Arduino.h>
#include "Stepper.h"

// X Diameter 40mm
// Y Diameter 12mm

class SteppersControl
{
public:
    SteppersControl(Stepper* xStepper, Stepper* yStepper);
    SteppersControl();
    ~SteppersControl();
    void goToSquare(int targetSquare);
    void calibrateAxes();
    void calibrateX();
    void calibrateY();
    void manualControl();

    SteppersControl& operator=(const SteppersControl& other);

private:
    Stepper* _xStepper;
    Stepper* _yStepper;
    const int stepsPerRev = 200;
    int _xAxisLocation;
    int _yAxisLocation;
    int _currentSquare;
};