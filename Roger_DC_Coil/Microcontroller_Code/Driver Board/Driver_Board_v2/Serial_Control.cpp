#include "Serial_Control.h"

Serial_Control::Serial_Control(int baud_rate = 9600, Magnet_Control* instance) {
    Magnet_Instance = instance; // Store the Magnet_Control instance
    init(baud_rate);            // Initialize serial communication
}

void Serial_Control::init(int baud_rate = 9600){
  Serial.begin(baud_rate);
  

}

bool Serial_Control::read_Serial() {
    if (Serial.available() > 0) {
        // Read the incoming JSON data from the serial buffer
        String input = Serial.readStringUntil('\n'); // Read until newline character

        // Deserialize the JSON document
        DeserializationError error = deserializeJson(read_data, input);

        // Check for errors in deserialization
        if (error) {
            Serial.print(F("deserializeJson() failed: "));
            Serial.println(error.f_str());
            return false;  // Return false to indicate failure
        }

        // Extract values from the JSON document
        bool state = read_data["state"];          // Example: 1
        bool magnet_mode = read_data["m_mode"];   // Example: 1
        bool polarity = read_data["pol"];         // Example: 1
        int power = read_data["pwr"];             // Example: 100
        float freq = read_data["freq"];           // Example: 1.01

        // Call the set_magnet method with the extracted values
        if (Magnet_Instance) {
            bool result = Magnet_Instance->set_magnet(state, magnet_mode, polarity, power, freq);
            return result;
        } else {
            Serial.println(F("Magnet_Instance is null."));
            return false;
        }
    } else {
        return false; // No data available
    }
}

#include <ArduinoJson.h>

bool Serial_Control::send_status(bool isOn, float voltage, float current, float hall, bool read_status) {
    // Create a StaticJsonDocument to hold the JSON structure

    // Populate the JSON document with input values
    send_data["isOn"] = isOn;
    send_data["voltage"] = voltage;
    send_data["current"] = current;
    send_data["hall"] = hall;
    send_data["read_status"] = read_status;

    // Serialize the JSON document to a string
    String output;
    serializeJson(send_data, output);

    // Send the serialized JSON string over serial
    Serial.println(output);

    // Optional: Debug output to Serial Monitor
    //Serial.print(F("Status sent: "));
    //Serial.println(output);

    return true; // Return true to indicate successful send
}


