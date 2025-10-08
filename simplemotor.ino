
int motorPin1 = 3;
int motorPin2 = 4;
int motorPin3 = 5;
int motorPin4 = 6;
//int enablePin = 5; // ENA connected to D5

void setup() {
    Serial.begin(9600);  // Initialize serial communication at 9600 baud
    pinMode(motorPin1, OUTPUT);
    pinMode(motorPin2, OUTPUT);
    pinMode(motorPin3, OUTPUT);
    pinMode(motorPin4, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the incoming command from Python code
    if (command == 'F') {
      // Move motor forward
      digitalWrite(motorPin1, HIGH);
      digitalWrite(motorPin2, LOW);
      digitalWrite(motorPin3, HIGH);
      digitalWrite(motorPin4, LOW); // To reverse motor, just set 3 to LOW and 4 to HIGH
      Serial.println("Forward command received");
    } else if (command == 'S') {
      // Stop motor
      digitalWrite(motorPin1, LOW);
      digitalWrite(motorPin2, LOW);
      digitalWrite(motorPin3, LOW);
      digitalWrite(motorPin4, LOW);
      Serial.println("Stop command received");
    }
  }
}
