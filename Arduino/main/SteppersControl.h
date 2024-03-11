#pragma once
#include <Arduino.h>

enum STEP_PINS { STEP_X_PIN = 2, STEP_Y_PIN, STEP_Z_PIN };
enum DIR_PINS { DIR_X_PIN = 5, DIR_Y_PIN, DIR_Z_PIN };
enum STEPS_PER_MM { X_STEPS_PER_MM = 10, Y_STEPS_PER_MM = 3 };
enum DIAMETERS { X_DIAMETER = 40, Y_DIAMETER = 12 }; // In mm
#define EN_PIN 8

// In mm
#define SQUARE_SIZE 34

// Steps per rev = 200 * 16
// 1.8 deg per step
#define STEPS_PER_REV 3200

class SteppersControl
{
public:
	// Constructor
	SteppersControl(const STEP_PINS xAxisStepPin, const DIR_PINS xAxisDirPin, const STEP_PINS yAxisStepPin, const DIR_PINS yAxisDirPin);

	// Methods
	void goToSquare(const int targetSquare);

private:
  // Variables
  int _xAxisStepPin;
  int _xAxisDirPin;
  int _yAxisStepPin;
  int _yAxisDirPin;

  int _xAxisLocation;
  int _yAxisLocation;
  int _currentSquare;

  // Methods
  void move(const bool xAxisDirection, const int xAxisDistance, const bool yAxisDirection, const int yAxisDistance);
};
