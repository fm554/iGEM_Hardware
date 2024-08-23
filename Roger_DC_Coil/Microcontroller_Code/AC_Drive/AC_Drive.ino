#include <Arduino.h>

// Pin declaration
const int EN = 4;     // pin for EN
const int INA = 9;    // pin for INA
const int INB = 10;   // pin for INB
const int Hall = A0;  // pin for hall probe

//Magnet State declaration
int state = 0;   // state of the magnet 1 - ON, 0 - OFF
bool mode = 0;   // mode of action, 0-AC, 1-DC
bool polarity = 0;// polarity of magnet, 0-N, 1-S
int power = 0;  // strength of the magnet -1 - -255 S, 1-255 N, 0 - OFF

// PWM wave parameters declearation
const int numSamples = 256;    // number of temporal divisions
const int samplingRate = 980;  // Sampling rate in 980 Hz, pin 5,6 pwm frequency
float frequency = 0.5;  // initial frequency = 0.5Hz
unsigned long previousMillis = 0;  // Store the last time the sine wave was updated
int currentIndex = 0;
unsigned long interval = 1000000 / (numSamples * frequency);
int16_t sineWave[numSamples];



// probe calculation decleration 
const float alpha = 0.7; // Smoothing factor for EMA, adjust as needed (0 < alpha < 1)
float ema = 0; // Exponential moving average
float gradient = -0.3407;
float zero = 512.44; //for hall effect sensor reading

// Function prototypes
void dc_control();
void pwm_control(unsigned long current_time);
void input_control();
void hall_sensor();
bool signal_processing();


void setup() {
  pinMode(EN, OUTPUT);
  pinMode(INA, OUTPUT);
  pinMode(INB, OUTPUT);  // initialize drive

  pinMode(Hall, INPUT);  // initialize hall probe

  Serial.begin(9600);  // initialize serial

  // Clear the prescaler bits (CS10, CS11, CS12)
  TCCR1B = TCCR1B & 0b11111000;
  // Set the prescaler to 1 (no prescaling)
  TCCR1B = TCCR1B | 0b00000001;  // fast pwm setting

  digitalWrite(EN, HIGH);  // EN 1 (OFF)
  digitalWrite(INA, LOW);  // INA 0
  digitalWrite(INB, LOW);  // INB 0 turn off the magnet

  for (int i = 0; i < numSamples; i++) {
    sineWave[i] = sin(2 * PI * i / numSamples) * 255;  // generate sine wave
    //Serial.println(sineWave[i]);
  }
  Serial.println("System Online!");
}

void loop() {
  if (state == 1) {
    if (mode == 0) {
      unsigned long currentMillis = micros();
      pwm_control(currentMillis, interval);
    } else if (mode == 1) {  // DC mode
      dc_control();
    }
  }

  if (Serial.available() > 0) {
    serial_processing();
  }
  hall_sensor();

}

void hall_sensor(){
  int currentReading = analogRead(Hall);
  ema = (alpha * currentReading) + ((1 - alpha) * ema);
  float reading = (ema - zero) * gradient;;
  Serial.println(reading);
}

void dc_control() {
  digitalWrite(EN, LOW);  // EN 0 (ON)
  if (polarity == "N") {
    analogWrite(INA, power * 2.55);
    digitalWrite(INB, LOW);
  } else if (polarity == "S") {
    digitalWrite(INA, LOW);
    analogWrite(INB, power * 2.55);
  }
}

void pwm_control(unsigned long current_time, unsigned long interval) {
  if (current_time - previousMillis >= interval) {
    previousMillis = current_time;

    int pwmValue = sineWave[currentIndex];  // Shift range from [-256, 256] to [0, 512]
    //pwmValue = map(pwmValue, 0, 512, 0, 255); // Map from [0, 512] to [0, 255]

    if (sineWave[currentIndex] >= 0) {
      analogWrite(INA, pwmValue * power / 100);
      digitalWrite(INB, LOW);
    } else {
      analogWrite(INB, -pwmValue * power / 100);
      digitalWrite(INA, LOW);
    }

    currentIndex = (currentIndex + 1) % numSamples;  // Move to the next sample
  }
}

void input_control() {
  String inco_msg = Serial.readString();
  inco_msg.trim();  // shape the input from serial port

  if (inco_msg == "ON") {
    Serial.println("ON");
    state = 1;
    digitalWrite(EN, LOW);  // EN 0 (ON)
  } else if (inco_msg == "OFF") {
    Serial.println("OFF");
    state = 0;
    previousMillis = 0;  // Reset the last time the sine wave was updated
    currentIndex = 0;
    digitalWrite(EN, HIGH);  // EN 1 (OFF)
    digitalWrite(INA, LOW);  // INA 0
    digitalWrite(INB, LOW);  // INB 0
  } else if (inco_msg.startsWith("AC ")) {
    String msg = inco_msg.substring(3);
    int firstSpaceIndex = msg.indexOf(' ');
    if (firstSpaceIndex != -1) {
      frequency = msg.substring(0, firstSpaceIndex).toFloat();  // Extract frequency
      mode = 0;
      power = msg.substring(firstSpaceIndex + 1).toInt();  // Extract power
      interval = 1000000 / (numSamples * frequency);       // Update interval based on new frequency
      Serial.print("AC set freq to(Hz): ");
      Serial.print(frequency);
      Serial.print("-interval:");
      Serial.print(interval);
      if (interval > 4294967295) {
        Serial.println("OVERFLOW");
      }
      else if(interval < 1){
        Serial.println("Too small Interval");
      }
      Serial.print("|Power is ");
      Serial.println(power * 2.55);
    }
  } else if (inco_msg.startsWith("DC ")) {
    polarity = inco_msg.substring(3, 4);    // Extract polarity
    //polarity.toUpperCase();                 // Convert polarity to uppercase
    power = inco_msg.substring(5).toInt();  // Correct calculation for mapping 0-100
    mode = 1;
    Serial.print("Polarity is ");
    Serial.print(polarity);
    Serial.print("|Power is ");
    Serial.println(power);
  } else if (inco_msg.startsWith("DC?")) {
    Serial.println(power * 2.55);
  }
}

bool isInteger(String str) {
  for (int i = 0; i < str.length(); i++) {
    if (!isDigit(str[i])) return false;
  }
  return true;
}

bool isFloat(String str) {
  bool dotSeen = false;
  for (int i = 0; i < str.length(); i++) {
    if (str[i] == '.') {
      if (dotSeen) return false;
      dotSeen = true;
    } else if (!isDigit(str[i])) {
      return false;
    }
  }
  return true;
}

void serial_processing() {
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