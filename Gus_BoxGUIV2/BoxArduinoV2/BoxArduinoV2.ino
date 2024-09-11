#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <Servo.h>

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

LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo filter_servo;
int position;
String target_motor;
void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  filter_servo.attach(12);  // attaches the servo on pin 9 to the servo object
  filter_servo.write(135);
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
//      calibrate_motor(target_motor);
    }
    else if (data.substring(0, 8) == "X Motor"){
      position = data.substring(9).toInt();
//      move_motor("X", position);
    }
    else if (data.substring(0, 8) == "Y Motor"){
      int position = data.substring(9).toInt();
//      move_motor("Y", position);
    }
    else {
      lcd.setCursor(0,1);
      lcd.print("___");
    }
  }
}
//
//void calibrate_motor(String target_motor){
// //from Lisa
//}
//
//void move_motor(String target_motor, int position){
////from Lisa
//}
