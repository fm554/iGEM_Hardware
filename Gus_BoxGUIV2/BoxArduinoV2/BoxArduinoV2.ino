#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <Servo.h>

//wiring notes
//lcd display: sda -> a4, scl -> a5
//x motor:???
//y motor:???
//x limit:???
//y limit:???
//servo motor -> pin9

//Message transmit list
// "Img: std"
// "Img: fluoro"

// "CoilA: on"
// "CoilA: off"
// "CoilB: on"
// "CoilB: off"

// "Calibrate: X"
// "X Motor: val"

int current_motor_position = 0
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Serial.begin(9600);
  lcd.init();
  lcd.backlight();
  filter_servo.attach(9);  // attaches the servo on pin 9 to the servo object
  filter_servo.write(135);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print(data);

    if (data == "Img: Std"){
      filter_servo.write(135); //out
    }
    else if  (data == "Img: fluoro"){
      filter_servo.write(180); //in
    }
    else if (data.substring(0,9) == "Calibrate"){
      target_motor = data.substring(11);
      calibrate_motor(target_motor);
    }
    else if (data.substring(0, 8) == "X Motor"){
      position = Convert.ToInt(data.substring(9));
      move_motor("X", position);
    }
    else if (data.substring(0, 8) == "Y Motor"){
      position = Convert.ToInt(data.substring(9));
      move_motor("Y", position);
    }
    else {
      lcd.setCursor(0,1);
      lcd.print("___");
    }
}

void calibrate_motor(String target_motor){
 //from Lisa
}

void move_motor(String target_motor, int position){
//from Lisa
}
