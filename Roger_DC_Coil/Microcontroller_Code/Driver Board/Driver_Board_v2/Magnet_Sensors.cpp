#include "Magnet_Sensors.h"

float Magnet_Sensors::average_read(uint8_t num_samples, uint8_t pin) {
  int sum = 0;
  for (uint8_t i = 0; i < num_samples; i++) {
    sum += analogRead(pin);
  }
  return sum / num_samples;
}

Magnet_Sensors::Magnet_Sensors(uint8_t switch_pin_input, uint8_t voltage_pin_input, uint8_t current_pin_input, uint8_t hall_pin_input) {
  switch_pin = switch_pin_input;    // initialize instance
  voltage_pin = voltage_pin_input;  // allocate pins
  current_pin = current_pin_input;
  hall_pin = hall_pin_input;

  init();
}

void Magnet_Sensors::init() {
  pinMode(switch_pin, INPUT);  //define pins
  pinMode(voltage_pin, INPUT);
  pinMode(current_pin, INPUT);
  pinMode(hall_pin, INPUT);

  //last_switch_state = digitalRead(switch_pin);  //initialize debounce
  //last_debounce_time = millis();
}

bool Magnet_Sensors::read_switch() {

  bool current_switch_state = digitalRead(switch_pin);  //read current value
  if (current_switch_state != last_switch_state) {      // implement
    last_debounce_time = millis();
  }
  if ((millis() - last_debounce_time) > debounce_delay) {
    if (current_switch_state != last_switch_state) {
      last_switch_state = current_switch_state;
    }
  }

  return last_switch_state;
}

float Magnet_Sensors::read_voltage() {
  int sensor_value = average_read(num_average_read, voltage_pin);
  float voltage = sensor_value* 5.0 / 1023.0 ; // 1024 -> 5
  float adjusted_voltage = voltage_sensitivity * (voltage - zero_voltage_offset); 
                  
  return adjusted_voltage;
}

float Magnet_Sensors::read_current() {
  int sensor_value = average_read(num_average_read, current_pin);
  float voltage = sensor_value* 5.0 / 1023.0;  // 1024 -> 5
  float adjusted_current = current_sensitivity * (voltage - zero_current_offset);
  return adjusted_current;
}

float Magnet_Sensors::read_hall() {
  int sensor_value = average_read(num_average_read, hall_pin);
  float voltage = sensor_value * 5.0 / 1023.0;  // 1024 -> 5
  float adjusted_magnetism = magnetism_sensitivity * (voltage - zero_magnetism_offset);
  return adjusted_magnetism;
}
