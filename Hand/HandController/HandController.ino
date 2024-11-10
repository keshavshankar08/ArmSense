#include <ESP32Servo.h>
// Function prototypes
void resting();
void Fist();
void Pointing();
void PeaceSign();
void ThumbsUp();

Servo finger1;  // create servo object to control a servo
Servo finger2;  // create servo object to control a servo
Servo finger3;  // create servo object to control a servo
Servo finger4;  // create servo object to control a servo
Servo finger5;  // create servo object to control a servo


void setup() {
  Serial.begin(115200);
  finger1.attach(4);  
  finger1.write(90);
  finger2.attach(5); 
  finger2.write(90);
  finger3.attach(18);  
  finger3.write(90);
  finger4.attach(19);  
  finger4.write(90);
  finger5.attach(21); 
  finger5.write(90);
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming data as a string until newline character
    String inputString = Serial.readStringUntil('\n');
    inputString.trim(); // Remove any leading/trailing whitespace

    // Convert the string to an integer
    int inputNumber = inputString.toInt();

    // Call the appropriate function based on the input number
    switch (inputNumber) {
      case 1:
        resting();
        break;
      case 2:
        Fist();
        break;
      case 3:
        Pointing();
        break;
      case 4:
        PeaceSign();
        break;
      case 5:
        ThumbsUp();
        break;
      default:
        Serial.println("Invalid input. Please enter a number between 1 and 5.");
        break;
    }
  }
}

void resting() {
  Serial.println("Resting Hand");
  finger1.write(90);
  finger2.write(90);
  finger3.write(90);
  finger4.write(90);
  finger5.write(90);
}

void Fist() {
  Serial.println("Fist");
  finger1.write(110);
  finger2.write(125);
  finger3.write(130);
  finger4.write(140);
  finger5.write(155);
}

void Pointing() {
  Serial.println("Pointing");
  finger1.write(110);
  finger2.write(125);
  finger3.write(130);
  finger4.write(90);
  finger5.write(155);
}

void PeaceSign() {
  Serial.println("Peace Sign");
  finger1.write(110);
  finger2.write(125);
  finger3.write(90);
  finger4.write(90);
  finger5.write(155);
}

void ThumbsUp() {
  Serial.println("Thumbs Up");
  finger1.write(110);
  finger2.write(125);
  finger3.write(130);
  finger4.write(140);
  finger5.write(90);

}