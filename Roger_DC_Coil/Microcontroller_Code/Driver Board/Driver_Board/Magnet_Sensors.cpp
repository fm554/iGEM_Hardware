#include "Magnet_Sensors.h"

Sensors::Sensors(int switch_pin_input, int voltage_pin_input, int current_pin_input, int hall_pin_input) {
  switch_pin = switch_pin_input;
  voltage_pin = voltage_pin_input;
  current_pin = current_pin_input;
  hall_pin = hall_pin_input;

  init();
}

void Sensors::init() {
  pinMode(switch_pin, INPUT);
  pinMode(voltage_pin, INPUT);
  pinMode(current_pin, INPUT);
  pinMode(hall_pin, INPUT);

  lastSwitchState = digitalRead(switch_pin);
  lastDebounceTime = millis();

  for (int i = 0; i < numReadings; i++) {
    current_readings[i] = 0;
  }
}

bool Sensors::read_switch() {
  bool currentSwitchState = digitalRead(switch_pin);
  
  if (currentSwitchState != lastSwitchState) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (currentSwitchState != lastSwitchState) {
      lastSwitchState = currentSwitchState;
    }
  }
  
  return lastSwitchState;
}

float Sensors::read_voltage() {
  int sensorValue = analogRead(voltage_pin);
  float voltage = sensorValue * (5.0 / 1023.0);

  float adjusted_voltage = (voltage - zero_voltage_offset) * sensitivity_multiplier;

  return adjusted_voltage;
}

float Sensors::read_current() {
  current_total -= current_readings[current_readIndex];

  current_readings[current_readIndex] = analogRead(current_pin);

  current_total += current_readings[current_readIndex];

  current_readIndex = (current_readIndex + 1) % numReadings;

  current_average = current_total / numReadings;

  float voltage = current_average * (5.0 / 1023.0);

  float current = (voltage - zeroCurrentVoltage) / sensitivity;

  return current;
}

float Sensors::read_hall() {
  int sensorValue = analogRead(hall_pin);
  float hall_voltage = sensorValue * (5.0 / 1023.0);
  return hall_voltage;
}
