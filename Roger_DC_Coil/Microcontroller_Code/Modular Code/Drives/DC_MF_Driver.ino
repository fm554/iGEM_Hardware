const int EN = 4; //pin for EN
const int INA = 5;// pin for INA
const int INB = 6;// pin for INB

int state = 0; // state of the motor 0 - Nothing, -1 - INB on, 1 - INA on
String inco_msg = "";

void setup() {
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  Serial.begin(9600);

  digitalWrite(EN,LOW); //EN 0 (always)
  digitalWrite(INA,LOW); //INA 0
  digitalWrite(INB,LOW); //INB 0
}

void loop() {

  if (Serial.available() > 0 ) {
    inco_msg = Serial.readString();
    inco_msg.trim(); //shape the input from serial port
    //Serial.print(inco_msg);
    if (inco_msg == "INA_ON") {
      Serial.print("INA_ON");
      Serial.print("  Current state is  ");
      state = 1;
      Serial.println(state);// OUTPUT to user
      digitalWrite(EN,LOW); //EN 0 (always)
      digitalWrite(INA,HIGH); //INA 0
      digitalWrite(INB,LOW); //INB 0
    } 
    else if (inco_msg == "INB_ON") {
      Serial.print("INB_ON");
      Serial.print("  Current state is  ");
      state = -1;
      Serial.println(state);
      digitalWrite(EN,LOW); //EN 0 (always)
      digitalWrite(INA,LOW); //INA 0
      digitalWrite(INB,HIGH); //INB 0
    } 
    else if (inco_msg == "OFF") {
      Serial.print("OFF");
      Serial.print("  Current state is  ");
      state = 0;
      Serial.println(state);
      digitalWrite(EN,HIGH); //EN 0 (always)
      digitalWrite(INA,LOW); //INA 0
      digitalWrite(INB,LOW); //INB 0
    }



  }


}
