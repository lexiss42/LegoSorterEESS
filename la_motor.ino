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
    //Handles number commands
    if (isDigit(command.charAt(1))) 
    {
        int num = Serial.parseInt();   
        if (num != 0) 
        {
            move(num);                
        }
    } else //Handles string command
    {
        if(command == "start"){
            start_conveyer();
        } 
        if(command == "stop"){
            stop_conveyer();
        }
    }  
  }
}

void move(int command) 
{
  myStepper.step(command * division);
}

void start_conveyer(){
    pass
}

void stop_conveyer(){
    pass
}


   
 
