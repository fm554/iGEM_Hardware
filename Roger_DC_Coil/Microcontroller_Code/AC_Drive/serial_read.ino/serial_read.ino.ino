bool state = 0;
bool mode = 0;
bool polarity = 0;
int power = 0;
float frequency = 0;

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  Serial.setTimeout(1000);
  delay(50);
  Serial.println("ONLINE");
}

void loop() {
  if (Serial.available()) {
    serial_processing();
  }
  digitalWrite(13, state);
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
  int endIndex = x.indexOf(",");
  int tokenIndex = 0;
  bool validInput = true;

  bool tempState = false, tempMode = false, tempPolarity = false;
  int tempPower = 0;
  float tempFrequency = 0.0;

  while (endIndex >= 0 && validInput) {
    String token = x.substring(startIndex, endIndex);
    token.trim();
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
        if (isFloat(token)) {
          int value = token.toFloat();
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
    endIndex = x.indexOf(',', startIndex);
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
    Serial.print(x);
    Serial.println("BADINPUT");
  }
}
