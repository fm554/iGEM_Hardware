#include <Stepper.h>

// Define number of steps per revolution:
const int stepsPerRevolution = 20;

// Initialize the stepper library on pins 8 through 11:
Stepper myStepper = Stepper(stepsPerRevolution, 5, 6, 10, 11);

void setup() {
  // Set the motor speed (RPMs):
  myStepper.setSpeed(400);
  myStepper.step(400);
}

void loop() {
  // Step one revolution in one direction:


//delay(2000);
//
//// Step on revolution in the other direction:
//myStepper.step(-stepsPerRevolution);
//
//delay(2000);
}
