// Include all the libraries
#include <Arduino.h>
#include "Magnet_Control.h"
#include "Magnet_Sensors.h"
#include "OLED_Display.h"
#include "Serial_Control.h"

// Define constants
const int SERIAL_BAUD_RATE = 9600;  // Define the baud rate

// Declare pins
int EN = 2;
int INA = 10;
int INB = 11;

int switch_pin = 3;
int current_pin = A0;
int voltage_pin = A1;
int hall_pin = A2;

// Declare instances of the classes
Magnet_Control magnetControl(EN, INA, INB); // Instance for controlling magnet
Magnet_Sensors magnetSensors(switch_pin, current_pin, voltage_pin, hall_pin); // Instance for managing sensors
OLED_Display oledDisplay; // Instance for OLED display
Serial_Control serialControl(SERIAL_BAUD_RATE, &magnetControl); // Instance for serial control, passing reference to magnetControl

// Setup variables
bool switch_status = false;
float voltage = 0.0;
float current = 0.0;
float hall = 0.0;
bool status = false;

void setup() {
  // Initialize Serial
  serialControl.init(SERIAL_BAUD_RATE);

  // Initialize OLED Display
  oledDisplay.init();

  // Initialize sensors (if needed)
  magnetSensors.init();

  // Perform any additional setup for magnet control
  magnetControl.init();
}

void loop() {
  // Read sensors
  switch_status = magnetSensors.read_switch();
  voltage = magnetSensors.read_voltage();
  current = magnetSensors.read_current();
  hall = magnetSensors.read_hall();

  // Handle serial communication
  if (Serial.available() > 0) { // Correct syntax for checking serial availability
    status = serialControl.read_Serial(); // Corrected function name
  }

  // Adjust state according to sensors
  // Logic: if current > 0.75A, turn off
  if (current >= 0.75) {
    magnetControl.turn_off();
  }

  // Turn off magnet if the switch is off
  if (!switch_status) {
    magnetControl.turn_off();
  }

  // Send status over serial
  serialControl.send_status(magnetControl.get_state(), magnetControl.get_mode(), voltage, current, magnetControl.get_frequency(), hall, status);

  // Update display
  oledDisplay.update_display(magnetControl.get_state(), magnetControl.get_mode(), voltage, current, magnetControl.get_frequency());

  // Update magnet control logic (if needed)
  magnetControl.update_magnet();


}
