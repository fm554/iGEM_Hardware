#include <LiquidCrystal_I2C.h>

#include <Wire.h>

//SETUP
//connect 5v and gnd
//sda to pin a4, slc to pin a5

LiquidCrystal_I2C lcd(0x27, 16, 2);


void setup() { 
  //initialize lcd screen
  lcd.init();
  // turn on the backlight
  lcd.backlight();

}
void loop() {
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Cambridge");
  lcd.setCursor(0,1);
  lcd.print("iGEM 2024");

  delay(2000);

  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("MaGenTa");
  delay(2000);
  //wait  for a second
//
//  delay(500);
//  lcd.setCursor(3,0);
//  lcd.print("iGEM 2024");
  // tell the screen to write on the top row
//  lcd.setCursor(0,0);
//  // tell the screen to write “hello, from” on the top  row
//  lcd.print("Hello, From");
//  // tell the screen to write on the bottom  row
//  lcd.setCursor(0, 1);
//  // tell the screen to write “Arduino_uno_guy”  on the bottom row
//  // you can change whats in the quotes to be what you want  it to be!
//  lcd.print("iGEM 2024");
  
}
