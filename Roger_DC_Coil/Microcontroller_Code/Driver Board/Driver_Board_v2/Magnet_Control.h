#ifndef MAGNET_CONTROL_H
#define MAGNET_CONTROL_H

#include <Arduino.h>

class Magnet_Control {
  private:
    // define pin
    uint8_t _INA;
    uint8_t _INB;
    uint8_t _EN;

    // declare the states of the magnet
    bool switch_state;
    bool state;
    bool magnet_mode;
    bool polarity;
    uint8_t power;
    float frequency;

    // parameters for generating waveform
    static const uint8_t num_samples = 64;
    const int sampling_rate = 980;
    int8_t waveform[64];

    // parameters for pwm control
    unsigned long current_millis = 0;
    unsigned long previous_millis = 0;
    int current_index = 0;
    unsigned long interval;

    //function for generating the waveform
    int8_t square_gen(uint8_t size, uint8_t position);
    int8_t sinusoidal_gen(uint8_t size, uint8_t position);
    int8_t triangular_gen(uint8_t size, uint8_t position);

  public:
    // initilizing instance
    Magnet_Control(uint8_t EN, uint8_t INA, uint8_t INB);

    void init();

    //waveform
    void set_waveform(byte wavetype);

    //operate parameters
    void set_DC(bool input_polarity, float input_power);
    void set_AC(float input_frequency, float input_power);
    void turn_on();
    void turn_off();
    bool set_magnet(bool state_input, bool mode_input, bool polarity_input, uint8_t power_input, float frequency_input);

    //update magnet state
    void update_magnet();

    //check magnet

    bool get_state();
    bool get_mode();
    bool get_polarity();
    float get_power();
    float get_frequency();
};

#endif 