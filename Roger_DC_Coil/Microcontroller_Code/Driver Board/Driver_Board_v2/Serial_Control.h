#ifndef SERIAL_CONTROL_H
#define SERIAL_CONTROL_H

#include <Arduino.h>
#include <ArduinoJson.h> // Include the ArduinoJson library
#include "Magnet_Control.h"  // Include the full definition

// Forward declare Magnet_Control to avoid circular dependency
class Magnet_Control;

class Serial_Control {
private:
    // Pointer to the Magnet_Control instance and the set_magnet method
    Magnet_Control* Magnet_Instance;


    // Store parsed data
    bool state;
    bool magnet_mode;
    bool polarity;
    int power;
    float freq;
public:
    // JSON documents for communication
    StaticJsonDocument<256> read_data;
    StaticJsonDocument<196> send_data;

    // Constructor
    Serial_Control(int baud_rate = 9600, Magnet_Control* instance = nullptr);

    // Initialize serial communication
    void init(int baud_rate);

    // Read instruction from host
    bool read_Serial();

    // Getter functions for parsed data
    bool getState() const { return state; }
    bool getMagnetMode() const { return magnet_mode; }
    bool getPolarity() const { return polarity; }
    int getPower() const { return power; }
    float getFreq() const { return freq; }

    // Send status to host
    bool send_status(float voltage, float current, float hall, bool read_status,
                     bool state, bool magnet_mode, bool polarity, int power, float freq);
};

#endif // SERIAL_CONTROL_H
