//This code returns a value of 0 if the button switch is open. If the button switch is closed, the value is 255. It is taking a measurement every "500".
#define sensorPin A0
//The coordinate value is the mm distance of the white block to the right of the origin site. I have arbitrarilly decided the origin is about 10mm to the.. 
//..right of the motor. 

//This bit is a problem. I want it to remember its previous value from previos.
//int position=9;

//Here are all the variables which I can set at the beginning:
//Calibrating=1 means I want calibration to occur. Calibrating=0 means I do not want it to occur.
int calibrating;
//This is the position that I would like the white stage to end up at.
int finalPosition;


//This is all initiating the motor, so that we can use it later. This will not need to be toutched, unless motor is changed.
#include <Stepper.h>
// Define number of steps per revolution:
const int stepsPerRevolution = 20;
const float revsPerMM= 1.9984;
int position = 0;

//!!! Deleted this out because it needs to change!!! const int MM= 15;
// Initialize the stepper library on pins 8 through 11:
Stepper myStepper = Stepper(stepsPerRevolution, 8, 9, 10, 11);



void setup() {
  //Setting up the motor speed
  myStepper.setSpeed(400);
  //Setting up the display
  }


void loop() {
  moving();
    }  


//All functions are down below here!

//Moving about function
void moving(){
  //This is where I ask if it would like to calibrate or not
  //Serial.println(position);
  Serial.end();
  Serial.begin(9600);
  Serial.print("Do you want to calibrate? 1=Yes, 0=No: ");
  while (Serial.available()==0){
  }
  calibrating=Serial.parseInt();
  Serial.print("I recieved: ");
  Serial.println(calibrating, DEC);
  // I shouldn't need this anymore because it is actually working! Serial.println(calibrating);
  delay(1000);
  //You have to end and re-start the serial page because otherwise it will keep the input from the last question and answer immediately.
  Serial.end();
  Serial.begin(9600);
  //This is where I ask if which position I would like it to go to
  Serial.print("Where would you like me to go? ");
  while (Serial.available()==0){
  }
  finalPosition=Serial.parseInt();
  Serial.print("I recieved: ");
  Serial.println(finalPosition, DEC);

  
  //If calibration loop is below
  if (calibrating==1){
    //Call the calibration function. 
    calibration();
    delay(1000);
    int MM=finalPosition;
    int StepsToMove= revsPerMM * MM * stepsPerRevolution;
    //Steps the number of steps. Positive value is towards zero, negative is away from zero. Opposite to logical way around. 
    myStepper.step(-StepsToMove);
    position=finalPosition;
    Serial.print("Final position: ");
    Serial.println(position);
    delay(1000);
    }
  else{
    delay(1000);
    Serial.print(position);
    int MM=finalPosition-position;
    int StepsToMove= revsPerMM * MM * stepsPerRevolution;
    //Steps the number of steps 
    myStepper.step(-StepsToMove);
    position=finalPosition;
    Serial.print("Position: ");
    Serial.println(position);
    delay(1000);
    }  
}

//ReadSensor function
int readSensor() {
  int sensorValue = analogRead(sensorPin);  
  int outputValue = map(sensorValue, 0, 1023, 255, 0); 
  return outputValue;     
}       

//Calibration function.
void calibration(){
  while(readSensor()<=150){
    //Number in myStepper should normally be positive. Positive is to the left, negative is to the right.
    myStepper.step(20);
  }
  position=0;
}



