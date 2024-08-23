#include "OLED_Display.h"

// Constructor to initialize the display
OLEDInterface::OLEDInterface() : u8g2(U8G2_R0, /* reset=*/ U8X8_PIN_NONE) {}

// Method to initialize the OLED display
void OLEDInterface::begin() {
  u8g2.begin();
}

// Method to update the display with new values
void OLEDInterface::updateDisplay(bool isOn, bool isAC, float voltage, float current, float frequency) {
  u8g2.clearBuffer(); // Clear the internal buffer

  // Draw horizontal divider line at 1/3rd of the height (around 21 pixels)
  u8g2.drawLine(0, 32, 42, 32);

  // Draw vertical divider line at 1/3rd of the width (64 pixels)
  u8g2.drawLine(42, 0, 42, 64);

  // Set font for text
  u8g2.setFont(u8g2_font_ncenB08_tr);

  // ON/OFF section
  if (isOn) {
    u8g2.setDrawColor(1); // Normal color
    u8g2.drawBox(0, 0, 42, 32); // Fill the ON/OFF section with black
    u8g2.setDrawColor(0); // Set color for text
    u8g2.setCursor(8, 21);
    u8g2.print("ON");
  } else {
    u8g2.setDrawColor(1); // Normal color
    u8g2.setCursor(8, 21); // Adjust position for "OFF"
    u8g2.print("OFF");
  }

  // AC/DC section
  u8g2.setDrawColor(1); // Normal color
  u8g2.setCursor(8, 56); // Adjust position for "AC/DC"
  if (isAC) {
    u8g2.print("AC");
  } else {
    u8g2.print("DC");
  }

  // Set smaller font for the other text
  u8g2.setFont(u8g2_font_helvR08_tf);

  // Display voltage
  u8g2.setCursor(50, 15);
  u8g2.print("Volt: ");
  u8g2.print(voltage);
  u8g2.print("V");

  // Display current
  u8g2.setCursor(50, 30);
  u8g2.print("Current: ");
  u8g2.print(current);
  u8g2.print("A");

  // Display frequency
  u8g2.setCursor(50, 50);
  u8g2.print("Freq: ");
  u8g2.print(frequency);
  u8g2.print("Hz");

  // Send the buffer to the display
  u8g2.sendBuffer();
}
