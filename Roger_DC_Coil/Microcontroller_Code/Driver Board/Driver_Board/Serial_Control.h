#ifndef SERIALPROCESSOR_H
#define SERIALPROCESSOR_H

#include <Arduino.h>

class SerialProcessor {
  public:
    SerialProcessor();

    void serial_processing();


  private:
    bool isInteger(const String &str);
    bool isFloat(const String &str);
};

#endif
