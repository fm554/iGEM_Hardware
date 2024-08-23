#include <Arduino.h>
#include "OLED_Display.h"    // Include the header for the OLEDInterface class
#include "Magnet_Sensors.h"  // Include the header for the Sensors class
#include "Serial_Control.h"  // Include the header for the SerialControl class
#include "Magnet_Control.h"  // Include the header for the MagnetController class

// Pin declaration
const int EN = 8;             // pin for EN
const int INA = 9;            // pin for INA
const int INB = 10;           // pin for INB
const int current_sensor = A1; // pin for current sensor
const int voltage_sensor = A0; // pin for voltage sensor
const int onboard_switch = 2;  // pin for onboard switch

// Global instances of the classes
OLEDInterface oledDisplay;
Sensors magnetSensors(onboard_switch, voltage_sensor, current_sensor, A2); // Assuming Hall sensor is on A2
SerialProcessor serialProcessor;
MagnetController magnetController(EN, INA, INB);

void setup() {
  // Initialize the OLED display
  oledDisplay.begin();

  // Initialize the sensors
  magnetSensors.init();

  // Initialize Serial communication
  Serial.begin(9600);
  serialControl.begin();

  // Initialize the magnet controller
  magnetController.init();

  // Initial display update
  oledDisplay.updateDisplay(false, false, 0.0, 0.0, 0.0);
}

void loop() {
  // Read the sensor values
  bool switchState = magnetSensors.read_switch();
  float voltage = magnetSensors.read_voltage();
  float current = magnetSensors.read_current();
  float hallValue = magnetSensors.read_hall();

  // Update the magnet controller based on some conditions (e.g., switch state)
  if (switchState) {
    magnetController.turn_on();
    // Set AC mode as an example, with a frequency of 1Hz and 50% power
    magnetController.set_AC(1.0, 50.0);
  } else {
    magnetController.turn_off();
  }

  // Update the magnet controller (handles AC waveform updates, etc.)
  magnetController.update_magnet();

  // Display the sensor values on the OLED
  oledDisplay.updateDisplay(switchState, magnetController.mode(), voltage, current, hallValue);

  // Handle serial communication (commands from the user, etc.)
  serialControl.processCommands();

  // Optional delay for readability
  //delay(1000); // Update every 1 second
}
