#ifndef SERIAL_CONTROL_H
#define SERIAL_CONTROL_H

#include <Arduino.h>
#include <ArduinoJson.h> // Include the ArduinoJson library

// Forward declare Magnet_Control to avoid circular dependency
class Magnet_Control;

class Serial_Control {
private:
    // Pointer to the Magnet_Control instance and the set_magnet method
    Magnet_Control* Magnet_Instance;

public:
    // JSON documents for communication
    StaticJsonDocument<96> read_data;
    StaticJsonDocument<96> send_data;

    // Constructor
    Serial_Control(int baud_rate, Magnet_Control* instance);

    // Initialize serial communication
    void init(int baud_rate);

    // Read instruction from host
    bool read_Serial();

    // Send status to host
    bool send_status(bool isOn, float voltage, float current, float hall, bool read_status);
};

#endif // SERIAL_CONTROL_H
