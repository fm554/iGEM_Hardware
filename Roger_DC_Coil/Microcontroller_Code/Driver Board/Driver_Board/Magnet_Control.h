#ifndef MAGNET_CONTROLLER_H
#define MAGNET_CONTROLLER_H

#include <Arduino.h>

class Magnet_Controller {
  private:
    int _INA;
    int _INB;
    int _EN;

    const int numSamples = 256;
    const int samplingRate = 980;

    unsigned long previousMillis = 0;
    int currentIndex = 0;
    unsigned long interval;
    int16_t waveform[256];

    bool switch_state;
    bool state;
    bool magnet_mode;
    bool polarity;
    int power;

    int16_t square(int size, int position);
    int16_t sinusoidal(int size, int position);
    int16_t triangular(int size, int position);

  public:
    float frequency = 0.5;

    Magnet_Controller(int EN, int INA, int INB);

    void init();
    void set_waveform(byte wavetype);
    void set_DC(bool input_polarity, float input_power);
    void set_AC(float input_frequency, float input_power);
    void update_magnet();
    String print_magnet_state();
    bool is_on();
    bool mode();
    bool get_polarity();
    float get_power();
    float get_frequency();
    void turn_on();
    void turn_off();
};

#endif
