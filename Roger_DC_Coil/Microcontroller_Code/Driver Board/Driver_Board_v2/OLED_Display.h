#ifndef OLED_DISPLAY_H
#define OLED_DISPLAY_H

#include <U8g2lib.h>
#include <Wire.h>

class OLED_Display {
private:
  U8G2_SH1106_128X64_NONAME_1_HW_I2C u8g2;  // U8g2 object for OLED control

public:

  //initialize oled display
  OLED_Display();

  void init();

  // update OLED display

  void update_display(bool isOn, bool isAC, float voltage, float current, float frequency, bool isConnected);
};

#endif 