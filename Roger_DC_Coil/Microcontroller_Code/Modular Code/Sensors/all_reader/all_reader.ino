#include <Arduino.h>

class sensors {
  private:
    int switch_pin;
    int voltage_pin;
    int current_pin;
    int hall_pin;
    unsigned long debounceDelay; // debounce delay in milliseconds
    bool lastSwitchState;
    unsigned long lastDebounceTime;
    bool stableSwitchState;

  public:
    sensors(int switch_pin_input, int voltage_pin_input, int current_pin_input, int hall_pin_input) 
      : switch_pin(switch_pin_input), voltage_pin(voltage_pin_input), current_pin(current_pin_input), hall_pin(hall_pin_input), debounceDelay(50), lastSwitchState(LOW), lastDebounceTime(0), stableSwitchState(LOW) {
      init();
    }

    void init() {
      pinMode(switch_pin, INPUT);
      pinMode(voltage_pin, INPUT);
      pinMode(current_pin, INPUT);
      pinMode(hall_pin, INPUT);

      lastSwitchState = digitalRead(switch_pin); // Initialize last switch state
      lastDebounceTime = millis();
      stableSwitchState = lastSwitchState;
    }

    bool read_switch() {
      bool currentSwitchState = digitalRead(switch_pin);
      
      if (currentSwitchState != lastSwitchState) {
        // Reset the debounce timer if the switch state has changed
        lastDebounceTime = millis();
      }

      // Check if the debounce time has passed
      if ((millis() - lastDebounceTime) > debounceDelay) {
        // If the switch state has been stable for longer than debounceDelay, update the stable state
        if (currentSwitchState != stableSwitchState) {
          stableSwitchState = currentSwitchState;
        }
      }

      lastSwitchState = currentSwitchState;
      return stableSwitchState;
    }

    float read_voltage() {
      int sensorValue = analogRead(voltage_pin);
      float voltage = sensorValue * (5.0 / 1023.0);  // assuming a 5V reference and 10-bit ADC
      return voltage;
    }

    float read_current() {
      int sensorValue = analogRead(current_pin);
      float current = sensorValue * (5.0 / 1023.0);  // This should be adjusted based on your current sensor's specification
      return current;
    }

    float read_hall() {
      int sensorValue = analogRead(hall_pin);
      float hall_voltage = sensorValue * (5.0 / 1023.0);  // assuming a 5V reference and 10-bit ADC
      return hall_voltage;
    }
};

// Create an instance of the sensors class
sensors mySensor(2, A0, A1, A2);  // Example pins

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Reading and printing sensor values
  Serial.print("Switch: ");
  Serial.print(mySensor.read_switch());
  Serial.print(", Voltage: ");
  Serial.print(mySensor.read_voltage());
  Serial.print("V, Current: ");
  Serial.print(mySensor.read_current());
  Serial.print("A, Hall: ");
  Serial.print(mySensor.read_hall());
  Serial.println("V");

  delay(100);
}
