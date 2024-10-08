#ifndef MAGNET_SENSORS_H
#define MAGNET_SENSORS_H

#include <Arduino.h>

class Magnet_Sensors {
private:
  //define pins to sensors
  uint8_t switch_pin;
  uint8_t voltage_pin;
  uint8_t current_pin;
  uint8_t hall_pin;


  // the rest of the parameters are for data processing
  // parameters for debouncing
  unsigned long debounce_delay = 50;
  bool last_switch_state;
  unsigned long last_debounce_time;

  //parameters for current measurement
  const float current_sensitivity = 0.18889;  //
  const float zero_current_offset = 2.46;

  //parameters for voltage measurements
  const float voltage_sensitivity = 21.59827;
  const float zero_voltage_offset = 0.0463;

  //parameters for magnetism measurement
  const float magnetism_sensitivity = 21.59827;
  const float zero_magnetism_offset = 0.0463;

  //average the reading
  float average_read(uint8_t num_samples, uint8_t pin);
  uint8_t num_average_read = 5;

public:
  //initialize instance
  Magnet_Sensors(uint8_t switch_pin_input, uint8_t voltage_pin_input, uint8_t current_pin_input, uint8_t hall_pin_input);

  void init();

  //read the sensor
  bool read_switch();
  float read_voltage();
  float read_current();
  float read_hall();
};

#endif 