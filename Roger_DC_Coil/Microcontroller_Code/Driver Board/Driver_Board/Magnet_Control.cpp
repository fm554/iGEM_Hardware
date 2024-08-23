#include "Magnet_Control.h"


Magnet_Controller::Magnet_Controller(int EN, int INA, int INB) {
  _INA = INA;
  _INB = INB;
  _EN = EN;
  init();
}

void Magnet_Controller::init() {
  state = 0;
  magnet_mode = 0;
  polarity = 0;
  power = 0;

  pinMode(_EN, OUTPUT);
  pinMode(_INA, OUTPUT);
  pinMode(_INB, OUTPUT);

  TCCR1B = TCCR1B & 0b11111000;
  TCCR1B = TCCR1B | 0b00000001;

  digitalWrite(_EN, HIGH);
  digitalWrite(_INA, LOW);
  digitalWrite(_INB, LOW);
}

int16_t Magnet_Controller::square(int size, int position) {
  if (position <= 0.5 * size) {
    return 255;
  } else {
    return -255;
  }
}

int16_t Magnet_Controller::sinusoidal(int size, int position) {
  return (int16_t)(255 * sin(2 * PI * position / size));
}

int16_t Magnet_Controller::triangular(int size, int position) {
  if (position <= 0.5 * size) {
    return (int16_t)(2 * 255 * position / size);
  } else {
    return (int16_t)(2 * 255 * (1 - (float)position / size));
  }
}

void Magnet_Controller::set_waveform(byte wavetype) {
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

void Magnet_Controller::set_DC(bool input_polarity, float input_power) {
  magnet_mode = 1;
  polarity = input_polarity;
  power = input_power;
}

void Magnet_Controller::set_AC(float input_frequency, float input_power) {
  magnet_mode = 0;
  frequency = input_frequency;
  power = input_power;
  interval = 1000000 / (numSamples * frequency);
}

void Magnet_Controller::update_magnet() {
  if (state == 1) {
    if (magnet_mode == 1) {
      if (polarity == 0) {
        analogWrite(_INA, power * 2.55);
        digitalWrite(_INB, LOW);
      } else {
        digitalWrite(_INA, LOW);
        analogWrite(_INB, power * 2.55);
      }
    } else if (magnet_mode == 0) {
      unsigned long currentMillis = millis();
      if (currentMillis - previousMillis >= interval) {
        previousMillis = currentMillis;

        int pwmValue = waveform[currentIndex];

        if (pwmValue >= 0) {
          analogWrite(_INA, pwmValue * power / 100);
          digitalWrite(_INB, LOW);
        } else {
          analogWrite(_INB, -pwmValue * power / 100);
          digitalWrite(_INA, LOW);
        }

        currentIndex = (currentIndex + 1) % numSamples;
      }
    }
  }
}

String Magnet_Controller::print_magnet_state() {
  String stateString = "State: " + String(state) + ", Mode: " + (magnet_mode ? "DC" : "AC") +
                       ", Polarity: " + (polarity ? "S" : "N") + ", Frequency: " + String(frequency) +
                       "Hz, Power: " + String(power) + "%";
  return stateString;
}

bool Magnet_Controller::is_on() {
  return state;
}

bool Magnet_Controller::mode() {
  return magnet_mode;
}

bool Magnet_Controller::get_polarity() {
  return polarity;
}

float Magnet_Controller::get_power() {
  return power;
}

float Magnet_Controller::get_frequency() {
  return frequency;
}

void Magnet_Controller::turn_on() {
  state = 1;
}

void Magnet_Controller::turn_off() {
  state = 0;
  digitalWrite(_INA, LOW);
  digitalWrite(_INB, LOW);
}
