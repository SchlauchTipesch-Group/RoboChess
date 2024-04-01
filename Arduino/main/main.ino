#include "SteppersControl.h"

SteppersControl sp = SteppersControl(STEP_X_PIN, DIR_X_PIN, STEP_Y_PIN, DIR_Y_PIN);

void setup()
{
  Serial.begin(115200);  
}

void loop()
{
  for (int i = 0; i < 64; i++)
  {
    sp.goToSquare(i);
    delay(1000);
  }

  delay(5000);
}
