#ifndef MAGNET_CONTROL_H
#define MAGNET_CONTROL_H

#include <Arduino.h>

class Magnet_Control {
private:
  // define pin
  int _INA;
  int _INB;
  int _EN;

  // declare the states of the magnet
  bool switch_state;
  bool state;
  bool magnet_mode;
  bool polarity;
  int power;
  float frequency;

  // parameters for generating waveform
  const int num_samples = 256;
  const int sampling_rate = 980;
  int16_t waveform[256];

  // parameters for pwm control
  unsigned long current_millis = 0;
  unsigned long previous_millis = 0;
  int current_index = 0;
  unsigned long interval;

  //function for generating the waveform
  int16_t square(int size, int position);
  int16_t sinusoidal(int size, int position);
  int16_t triangular(int size, int position);

public:
  // initilizing instance
  Magnet_Control(int EN, int INA, int INB);

  void init();

  //waveform
  void set_waveform(byte wavetype);

  //operate parameters
  void set_DC(bool input_polarity, float input_power);
  void set_AC(float input_frequency, float input_power);
  void turn_on();
  void turn_off();
  void set_magnet(bool state_input, bool mode_input, bool polarity_input, int power, float frequency);

  //update magnet state
  void update_magnet();

  //check magnet

  bool get_state();
  bool get_mode();
  bool get_polarity();
  float get_power();
  float get_frequency();
}

#endif 