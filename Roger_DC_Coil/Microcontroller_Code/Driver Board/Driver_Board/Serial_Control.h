#ifndef SERIALPROCESSOR_H
#define SERIALPROCESSOR_H

#include <Arduino.h>

class SerialProcessor {
  public:
    bool state;
    bool mode;
    bool polarity;
    int power;
    float frequency;

    SerialProcessor();

    void serial_processing();

  private:
    bool isInteger(const String &str);
    bool isFloat(const String &str);
};

#endif
