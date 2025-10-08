#include <Stepper.h>
// Define number of steps per revolution:
// Motor moves 1.8 degrees per step
const int stepsPerRevolution = 200;
const int division = 200/12; // Partitioned into 12 "slices"

// Initialize the stepper library on pins x:
Stepper myStepper = Stepper(stepsPerRevolution, 13, 12, 11, 10);

void setup() {
  // Set the motor speed (RPMs):
  myStepper.setSpeed(100);
  Serial.begin(9600);
}



void loop() 
{
  // Debug
  // Step one revolution in one direction:
  // myStepper.step(division);
  //  delay(2000);

  // Serial
  
  if (Serial.available() > 0) 
  {
    String command = Serial.readStringUntil('\n'); // read until newline
    command.trim();
    int num = Serial.parseInt();
    // Serial.parseInt() ignores non numbers
    if (num != 0)
    {    
      move(num);
    }
    
  }
}

void move(int steps) 
{
  myStepper.step(steps * division);
}


   
 
