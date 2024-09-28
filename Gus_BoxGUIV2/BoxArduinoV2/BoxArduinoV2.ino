#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <Servo.h>
#include <Stepper.h>

//wiring notes
//lcd display: sda -> a4, scl -> a5
//x motor: 2,3,4,5
//y motor:6,7,8,9
//x limit:10
//y limit:11
//servo motor -> 12

//Message transmit list
// "Img: std"
// "Img: fluoro"

// "CoilA: on"
// "CoilA: off"
// "CoilB: on"
// "CoilB: off"

// "Calibrate: X"
// "X Motor: val"

#define xSensorPin A1
#define ySensorPin A0

LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo filter_servo;
const int stepsPerRevolution = 20;
const float revsPerMM= 1.9984;
//Stepper xstepper = Stepper(20, 2,3,4,5);
//Stepper ystepper = Stepper(20, 6,7,8,9);

float x_position;
float y_position;
float to_position;
String target_motor;

void setup() {
  Serial.begin(9600);
  
  lcd.init();
  lcd.backlight();
  
  filter_servo.attach(12);  // attaches the servo on pin 9 to the servo object
  filter_servo.write(135);

//  xstepper.setSpeed(400);
//  ystepper.setSpeed(400);
//  calibrate("X");
//
//  move_motor("X", 300);
//  move_motor("X", 0);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print(data);
    

    if (data == "Img: std"){
      filter_servo.write(120); //out
    }
    else if  (data == "Img: fluoro"){
      filter_servo.write(177); //in
    }
    else if (data.substring(0,9) == "Calibrate"){
      String target_motor = data.substring(11);
//      calibrate(target_motor);
    }
    else if (data.substring(0, 7) == "X Motor"){
      to_position = data.substring(9).toFloat();
//      move_motor("X", to_position);
    }
    else if (data.substring(0, 7) == "Y Motor"){
      to_position = data.substring(9).toFloat();
//      move_motor("Y", to_position);
    }
    else {
      lcd.setCursor(0,1);
      lcd.print("___");
    }
  }
}


int readSensor(int sensor) {
  int sensorValue;
  if (sensor == 0){
    sensorValue = analogRead(xSensorPin);
  }
  else {
    sensorValue = analogRead(ySensorPin);
  }
  int outputValue = map(sensorValue, 0, 1023, 255, 0); 
  return outputValue;     
}       

//void calibrate(String target_motor){
//  if (target_motor == "X"){
//    if (readSensor(0)>=150){
//      xstepper.step(300);
//    }
//    while(readSensor(0)<=150){
//      xstepper.step(-20);
//    }
//    x_position = 0;
//  }
//  else if (target_motor == "Y"){
//    if (readSensor(1)>=150){
//      ystepper.step(300);
//    }
//    while(readSensor(1)<=150){
//      ystepper.step(-20);
//    }
//    y_position = 0;
//  }
//}

//void move_motor(String target_motor, float to_position){
//  if (target_motor == "X"){
//    int steps_to_move = (to_position-x_position)*revsPerMM*stepsPerRevolution;
//    xstepper.step(steps_to_move);
//    x_position = to_position;
//  }
//  else if (target_motor == "Y"){
//    int steps_to_move = (to_position-y_position)*revsPerMM*stepsPerRevolution;
//    ystepper.step(steps_to_move);
//    y_position = to_position;
//  }
//}


//
//void calibrate_motor(String target_motor){
// //from Lisa
//}
//
//void move_motor(String target_motor, int position){
////from Lisa
//}
