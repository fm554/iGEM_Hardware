#include "Serial_Control.h"
#include "Magnet_Control.h"  // Include the full definition
#include <ArduinoJson.h>
Serial_Control::Serial_Control(int baud_rate, Magnet_Control* instance):Magnet_Instance(instance) {
    init(baud_rate);            // Initialize serial communication
}

void Serial_Control::init(int baud_rate){
  Serial.begin(baud_rate);
  

}




bool Serial_Control::read_Serial() {
    const int bufferSize = 200;  // Define a reasonable buffer size for input
    static char input[bufferSize];  // Static to retain data between function calls
    static int index = 0;  // Static index to keep track of the buffer
    static bool processing = false;  // Flag to indicate if processing is ongoing

    // Read available data from the serial buffer
    while (Serial.available() > 0) {
        char c = Serial.read();  // Read one character at a time

        // If the first semicolon is detected and processing flag is false
        if (c == '\n' && !processing) {
            input[index] = '\0';  // Null-terminate the string
            processing = true;  // Set processing flag to true

            // Deserialize the complete JSON string
            DeserializationError error = deserializeJson(read_data, input);

            if (error) {
                Serial.println(F("deserializeJson() failed: "));
                Serial.println(input);  // Debug print the faulty input
                Serial.println(error.f_str());

                // Clear the input buffer for the next read
                index = 0;  // Reset index
                input[0] = '\0';  // Clear input
                processing = false;  // Reset processing flag
                return false;
            }

            // Successfully parsed JSON, proceed with extracted data
            state = read_data["state"];
            magnet_mode = read_data["m_mode"];
            polarity = read_data["pol"];
            power = read_data["pwr"];
            freq = read_data["freq"];

            // Clear input buffer after processing
            index = 0;  // Reset index
            input[0] = '\0';  // Clear input
            processing = false;  // Reset processing flag

            Serial.flush();  // Clear the serial buffer after processing
            return true;
        } else if (!processing) {
            // Only add characters if within buffer size limit and processing flag is false
            if (index < bufferSize - 1) {
                input[index++] = c;  // Append character to input buffer and increment index
            } else {
                // Buffer overflow, reset input and index
                Serial.println(F("Input buffer overflow, clearing input."));
                index = 0;  // Reset index
                input[0] = '\0';  // Clear input
                return false;
            }
        }
        // If processing flag is true, ignore subsequent characters until buffer is reset
    }

    return false;  // Return false if no complete JSON was read
}





bool Serial_Control::send_status(float voltage, float current, float hall, bool read_status,
                     bool state, bool magnet_mode, bool polarity, int power, float freq) {
    // Create a StaticJsonDocument to hold the JSON structure

    // Populate the JSON document with input values
    send_data["voltage"] = voltage;
    send_data["current"] = current;
    send_data["hall"] = hall;
    send_data["read_status"] = read_status;

    // Add new input parameters to the JSON document
    send_data["state"] = state;
    send_data["magnet_mode"] = magnet_mode;
    send_data["polarity"] = polarity;
    send_data["power"] = power;
    send_data["freq"] = freq;

    // Serialize the JSON document to a string
    const size_t outputSize = 196;  // Increased size to accommodate additional data
    char output[outputSize];
    serializeJson(send_data, output, outputSize);

    // Send the serialized JSON string over serial
    Serial.println(output);

    // Optional: Debug output to Serial Monitor
    //Serial.print(F("Status sent: "));
    //Serial.println(output);

    return true; // Return true to indicate successful send
}



