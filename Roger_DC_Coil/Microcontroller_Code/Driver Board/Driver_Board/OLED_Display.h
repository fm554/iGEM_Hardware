#ifndef OLEDINTERFACE_H
#define OLEDINTERFACE_H

#include <U8g2lib.h>
#include <Wire.h>

class OLEDInterface {
  public:
    // Constructor to initialize the display
    OLEDInterface();

    // Method to initialize the OLED display
    void begin();

    // Method to update the display with new values
    void updateDisplay(bool isOn, bool isAC, float voltage, float current, float frequency);

  private:
    U8G2_SH1106_128X64_NONAME_F_HW_I2C u8g2; // U8g2 object for OLED control
};

#endif
