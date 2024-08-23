#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>

class Sensors {
  private:
    int switch_pin;
    int voltage_pin;
    int current_pin;
    int hall_pin;
    unsigned long debounceDelay = 50;
    bool lastSwitchState;
    unsigned long lastDebounceTime;

    const float sensitivity = 0.18889;
    const float zeroCurrentVoltage = 2.46;

    const float zero_voltage_offset = 0.0774;
    const float sensitivity_multiplier = 0.0463;

    const int numReadings = 10;
    float current_readings[10];
    int current_readIndex = 0;
    float current_total = 0;
    float current_average = 0;

  public:
    Sensors(int switch_pin_input, int voltage_pin_input, int current_pin_input, int hall_pin_input);

    void init();
    bool read_switch();
    float read_voltage();
    float read_current();
    float read_hall();
};

#endif
