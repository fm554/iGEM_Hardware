const int currentPin = A1;  // Analog input pin that the sensor is connected to
const float sensitivity = 0.18889; // Sensitivity for ACS712-05B variant is 185mV/A

const float zeroCurrentVoltage = 2.46;  // This is the voltage at 0A current, Vcc/2 (2.5V for a 5V supply)

const int numReadings = 10;  // Number of readings to average
float readings[numReadings];  // Array to store the sensor readings
int readIndex = 0;  // Index of the current reading
float total = 0;  // Total of the readings
float average = 0;  // The average of the readings

void setup() {
  Serial.begin(9600);  // Start serial communication

  // Initialize all the readings to 0
  for (int i = 0; i < numReadings; i++) {
    readings[i] = 0;
  }
}

void loop() {
  // Subtract the last reading from the total
  total -= readings[readIndex];

  // Read the analog input from the sensor
  readings[readIndex] = analogRead(currentPin);

  // Add the current reading to the total
  total += readings[readIndex];

  // Advance to the next position in the array
  readIndex = (readIndex + 1) % numReadings;

  // Calculate the average
  average = total / numReadings;

  // Convert the averaged reading to a voltage
  float voltage = average * (5.0 / 1023.0);

  // Calculate the current in Amps
  float current = (voltage - zeroCurrentVoltage) / sensitivity;

  // Print the current value
  Serial.print("Filtered Current: ");
  Serial.print(current);
  Serial.println(" A");

  delay(100);  // Delay before the next reading
}
