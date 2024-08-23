int Hall_sensor = A0;

const float alpha = 0.7; // Smoothing factor for EMA, adjust as needed (0 < alpha < 1)
float ema = 0; // Exponential moving average
float gradient = -0.3407;
float zero = 512.44;

void setup() {
  pinMode(Hall_sensor, INPUT);
  Serial.begin(9600);
  Serial.println("System Online");

  // Initialize the EMA with the first reading
  ema = analogRead(Hall_sensor);

  float val1 = 655;
  float val2 = 512;
  float val3 = 331;
  Serial.print(linear_map(val1));
  Serial.print(linear_map(val2));
  Serial.print(linear_map(val3));
}

void loop() {
  // Read the current value
  int currentReading = analogRead(Hall_sensor);

  // Apply EMA filter
  ema = (alpha * currentReading) + ((1 - alpha) * ema);

  // Adjust the EMA value by subtracting 512
  //float adjustedEma = ema;
  float reading = linear_map(ema);
  // Print the adjusted EMA value
  //float val1 = 655;
  //float val2 = 512;
  //float val3 = 331;
  Serial.println(reading);

  // Delay for stability
  //delay(100);
}

float linear_map(float value){
  return (value - zero) * gradient;
}
