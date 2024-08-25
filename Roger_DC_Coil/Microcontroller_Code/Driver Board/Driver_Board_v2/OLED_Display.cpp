#include "OLED_Display.h"
#include <U8g2lib.h>
#include <Wire.h>
// Constructor to initialize the display
OLED_Display::OLED_Display()
  : u8g2(U8G2_R0, /* reset=*/U8X8_PIN_NONE) {}

// Method to initialize the OLED display
void OLED_Display::init() {
  u8g2.begin();
}



void OLED_Display::update_display(bool isOn, bool isAC, float voltage, float current, float frequency, bool isConnected) {
  u8g2.clearBuffer();  // Clear the internal buffer

  // Draw horizontal divider line at 1/3rd of the height (around 32 pixels)
  u8g2.drawLine(0, 32, 128, 32);

  // Draw vertical divider line at 1/3rd of the width (around 42 pixels)
  u8g2.drawLine(42, 0, 42, 64);

  // Set font for the left side text (bigger and bold font)
  u8g2.setFont(u8g2_font_courB12_tf);

  // ON/OFF section
  if (isOn) {
    // Draw a filled white box for "ON" state
    u8g2.setDrawColor(1);        // Set draw color to white (default)
    u8g2.drawBox(0, 0, 42, 32);  // Fill the box with white
    u8g2.setDrawColor(0);        // Set draw color to black for text
    u8g2.drawStr(10, 20, "ON");  // Draw "ON" text
  } else {
    // Draw "OFF" without filling the background
    u8g2.setDrawColor(1);  // Normal color for text
    u8g2.drawStr(10, 20, "OFF");
  }

  // AC/DC section
  if (isAC) {
    u8g2.setDrawColor(1);  // Normal color for text
    u8g2.drawStr(10, 52, "AC");
  } else {
    u8g2.setDrawColor(1);  // Normal color for text
    u8g2.drawStr(10, 52, "DC");
  }

  // Set font for the right side text (smaller font)
  u8g2.setFont(u8g2_font_6x10_tr);

  // Display current
  u8g2.setCursor(50, 15);
  u8g2.print("CURRENT");
  u8g2.setCursor(105, 15);
  u8g2.print(current, 2);
  u8g2.print(" A");

  // Display voltage
  u8g2.setCursor(50, 30);
  u8g2.print("VOLTAGE");
  u8g2.setCursor(105, 30);
  u8g2.print(voltage, 2);
  u8g2.print(" V");

  // Display frequency
  u8g2.setCursor(50, 45);
  u8g2.print("FREQ");
  u8g2.setCursor(105, 45);
  u8g2.print(frequency, 2);
  u8g2.print(" Hz");

  // Display connection status at the bottom
  if (isConnected) {
    u8g2.drawStr(50, 62, "CONNECTED");
  } else {
    u8g2.drawStr(50, 62, "DISCONNECTED");
  }

  // Send the buffer to the display
  u8g2.sendBuffer();
}
