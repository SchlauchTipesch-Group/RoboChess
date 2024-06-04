## Stepper Motor Control with Arduino

## Overview

This project demonstrates how to control two stepper motors using an Arduino board. The stepper motors are used to move a mechanism across a 64-square grid, where each square represents a specific location or position.

## Dependencies

- Arduino IDE
- Arduino board (e.g., Arduino Uno, Arduino Nano)
- Two stepper motors
- Stepper motor drivers (if required)

## Installation

1. Connect the stepper motors to the Arduino board according to the pin assignments specified in the code.
2. Upload the provided code to the Arduino board using the Arduino IDE.

## Functions

### SteppersControl(const STEP_PINS xAxisStepPin, const DIR_PINS xAxisDirPin, const STEP_PINS yAxisStepPin, const DIR_PINS yAxisDirPin)

The constructor function initializes the `SteppersControl` object with the pin assignments for the step and direction pins of the stepper motors for both the X and Y axes. It also sets up the initial locations and enables the stepper motor drivers.

### void goToSquare(const int targetSquare)

This function moves the mechanism to the specified square on the 64-square grid. The `targetSquare` parameter is an integer between 0 and 63, representing the target square's index. It calculates the row and column of the target square and calls the `move` function with the appropriate distances.

### void move(const bool xAxisDirection, const int xAxisDistance, const bool yAxisDirection, const int yAxisDistance)

This function handles the movement of the stepper motors along the X and Y axes. The `xAxisDirection` and `yAxisDirection` parameters specify the direction of movement (true for positive, false for negative). The `xAxisDistance` and `yAxisDistance` parameters specify the distance to move in millimeters. It sets the direction pins for each axis and then steps the motors simultaneously to reach the desired position. The current locations are updated after the movement is completed.

## Configuration

The following constants can be adjusted to customize the behavior of the stepper motor control:

- `EN_PIN`: The pin number for the enable pin of the stepper motor drivers.
- `X_STEPS_PER_MM`: The number of steps required for the stepper motor to move 1 millimeter along the X-axis.
- `Y_STEPS_PER_MM`: The number of steps required for the stepper motor to move 1 millimeter along the Y-axis.
- `SQUARE_SIZE`: The size of each square on the grid in millimeters.

## Contributions

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the project's GitHub repository.

## License

This project is licensed under the [MIT License](LICENSE).