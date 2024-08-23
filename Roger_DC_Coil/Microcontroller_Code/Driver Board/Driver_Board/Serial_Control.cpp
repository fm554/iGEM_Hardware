#include "Serial_Control.h"

SerialProcessor::SerialProcessor() {
  state = false;
  mode = false;
  polarity = false;
  power = 0;
  frequency = 0.0;
}

bool SerialProcessor::isInteger(const String &str) {
  for (unsigned int i = 0; i < str.length(); i++) {
    if (!isDigit(str[i])) return false;
  }
  return true;
}

bool SerialProcessor::isFloat(const String &str) {
  bool decimalPoint = false;
  for (unsigned int i = 0; i < str.length(); i++) {
    if (str[i] == '.') {
      if (decimalPoint) return false; // More than one decimal point
      decimalPoint = true;
    } else if (!isDigit(str[i])) {
      return false;
    }
  }
  return true;
}

void SerialProcessor::serial_processing() {
  String x = Serial.readStringUntil('\n');
  x.trim();

  if (x.length() == 0) {
    Serial.println("BADINPUT");
    return;
  }

  int startIndex = 0;
  int endIndex = x.indexOf(';');
  int tokenIndex = 0;
  bool validInput = true;

  bool tempState = false, tempMode = false, tempPolarity = false;
  int tempPower = 0;
  float tempFrequency = 0.0;

  while (endIndex >= 0 && validInput) {
    String token = x.substring(startIndex, endIndex);
    switch (tokenIndex) {
      case 0:
        if (isInteger(token)) {
          int value = token.toInt();
          if (value >= 0 && value <= 1) tempState = value;
          else validInput = false;
        } else validInput = false;
        break;
      case 1:
        if (isInteger(token)) {
          int value = token.toInt();
          if (value >= 0 && value <= 1) tempMode = value;
          else validInput = false;
        } else validInput = false;
        break;
      case 2:
        if (isInteger(token)) {
          int value = token.toInt();
          if (value >= 0 && value <= 1) tempPolarity = value;
          else validInput = false;
        } else validInput = false;
        break;
      case 3:
        if (isInteger(token)) {
          int value = token.toInt();
          if (value >= 0 && value <= 100) tempPower = value;
          else validInput = false;
        } else validInput = false;
        break;
      case 4:
        if (isFloat(token)) {
          float value = token.toFloat();
          if (value >= 0.001 && value <= 100) tempFrequency = value;
          else validInput = false;
        } else validInput = false;
        break;
      default:
        validInput = false;
        break;
    }
    startIndex = endIndex + 1;
    endIndex = x.indexOf(';', startIndex);
    tokenIndex++;
  }

  if (validInput && tokenIndex == 4) {
    String token = x.substring(startIndex);
    if (isFloat(token)) {
      float value = token.toFloat();
      if (value >= 0.001 && value <= 100) tempFrequency = value;
      else validInput = false;
    } else validInput = false;
    tokenIndex++;
  }

  if (validInput && tokenIndex == 5) {
    state = tempState;
    mode = tempMode;
    polarity = tempPolarity;
    power = tempPower;
    frequency = tempFrequency;
    Serial.println("READOK");
  } else {
    Serial.println("BADINPUT");
  }
}
