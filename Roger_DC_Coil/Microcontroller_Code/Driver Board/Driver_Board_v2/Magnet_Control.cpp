#include "Magnet_Control.h"
// initialize instance
Magnet_Control::Magnet_Control(int EN, int INA, int INB) {
  _INA = INA;
  _INB = INB;
  _EN = EN;
  init();
}

// generate one of three wave forms
int16_t Magnet_Control::square(int size, int position) {
  /**
  generate one wavelength of square wave. 
  input : size - total number of points
          position - current point
  output:
          value of curve at position
  **/
  if (position <= 0.5 * size) {
    return 100;  // all max amplitude = 100
  } else {
    return -100;
  }

  int16_t Magnet_Control::sinusoidal(int size, int position) {
    /**
  generate one wavelength of sine wave. 
  input : size - total number of points
          position - current point
  output:
          value of curve at position
  **/
    return (int16_t)(100 * sin(2 * PI * position / size));
  }

  int16_t Magnet_Control::triangular(int size, int position) {
    /**
  generate one wavelength of triangular wave. 
  input : size - total number of points
          position - current point
  output:
          value of curve at position
  **/
    if (position <= 0.5 * size) {
      return (int16_t)(4 * 100 * position / size - 100);
    } else {
      return (int16_t)(4 * 100 * (1 - (float)position / size) - 100);
    }
  }
  // initialize pins and registers
  void Magnet_Control::init() {
    switch_state;          // put the switch state into the main loop instead of magnet
    state = 0;             //off
    magnet_mode = 0;       // DC
    polarity = 0;          //N
    power = 0;             //pwr = 0
    frequency = 1.0;       //freq = 1hz
    pinMode(_EN, OUTPUT);  //initialize pins
    pinMode(_INA, OUTPUT);
    pinMode(_INB, OUTPUT);

    TCCR1B = TCCR1B & 0b11111000;  // set registers to adjust pwm frequency
    TCCR1B = TCCR1B | 0b00000001;

    turn_off();  // turn off magnet
  }

  void Magnet_Control::set_waveform(byte wavetype) {
    /**
  use one of the wave type to generate waveform
  input: wavetype - id of waveform : 0 - square, 1 - sine, 2 - triangular, others - line at 0
  output: will dump waveform data into waveform[] and can be used in the future
  **/

    switch (wavetype) {
      case 0:
        for (int i = 0; i < numSamples; i++) {
          waveform[i] = square(numSamples, i);
        }
        break;
      case 1:
        for (int i = 0; i < numSamples; i++) {
          waveform[i] = sinusoidal(numSamples, i);
        }
        break;
      case 2:
        for (int i = 0; i < numSamples; i++) {
          waveform[i] = triangular(numSamples, i);
        }
        break;
      default:
        for (int i = 0; i < numSamples; i++) {
          waveform[i] = 0;
        }
        break;
    }
  }
}

void Magnet_Control::set_DC(bool input_polarity, float input_power) {
  magnet_mode = 0;            //DC
  polarity = input_polarity;  // set polarity
  power = input_power         // set power
}

void Magnet_Control::set_AC(float input_frequency, float input_power) {
  magnet_mode = 1;  //AC
  frequency = input_frequency;
  power = input_power;
  interval = 1000000 / (num_samples * frequency)
}

void Magnet_Control::turn_on() {
  state = 1;
}

void Magnet_Control::turn_off() {
  state = 0;
  digitalWrite(_EN, HIGH);  // turn off magnet
  digitalWrite(_INA, LOW);
  digitalWrite(_INB, LOW);
}

void Magnet_Control::update_magnet() {
  if (state == 1) {          // if magnet is on
    if (magnet_mode == 0) {  // if DC
      if (polarity == 0) {
        analogWrite(_INA, power * 2.55);  // N, power from 100 -> 255
        digitalWrite(_INB, LOW);
      } else {
        digitalWrite(_INA, LOW);  //S , power from 100 -> 255
        analogWrite(_INB, power * 2.55);
      }
    } else if (magnet_mode == 1) {
      current_millis = millis();
      if (current_millis - previous_millis >= interval) {  // if time's up
        previous_millis = current_millis;

        int pwm_value = waveform[current_index];

        if (pwm_value >= 0) {
          analogWrite(_INA, pwm_value * power * 2.55);  // N, power from 100 -> 255
          digitalWrite(_INB, LOW);
        } else {
          analogWrite(_INB, -pwm_value * power * 2.55);  // N, power from 100 -> 255
          digitalWrite(_INA, LOW);
        }

        currentIndex = (currentIndex + 1) % numSamples;  // go to next index
      }
    }
  }
}

bool Magnet_Control::set_magnet(bool state_input, bool mode_input, bool polarity_input, int power_input, float frequency_input){
  state = state_input;
  magnet_mode = mode_input;
  polarity = polarity_input;
  power = power_input;
  frequency = frequency_input

  if (magnet_mode == 0){ //DC
    set_DC(polarity, power);
  }else if(magnet_mode == 1){//AC
    set_AC(frequency, power);
  }else{
    return 0
  }
  return 1
}

bool Magnet_Control::get_state() {
  return state;
}

bool Magnet_Control::get_mode() {
  return magnet_mode;
}

bool Magnet_Control::get_polarity() {
  return polarity;
}

float Magnet_Control::get_power() {
  return power;
}

float Magnet_Control::get_frequency() {
  return frequency;
}
