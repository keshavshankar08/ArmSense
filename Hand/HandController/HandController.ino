/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 https://www.arduino.cc/en/Tutorial/LibraryExamples/Sweep

 1 - 110
 2 - 125
 3 - 130
 4 - 140
 5 - 155

*/

#include <ESP32Servo.h>

Servo finger1;  // create servo object to control a servo
Servo finger2;  // create servo object to control a servo
Servo finger3;  // create servo object to control a servo
Servo finger4;  // create servo object to control a servo
Servo finger5;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position

void setup() {
  finger1.attach(4);  // attaches the servo on pin 9 to the servo object
  finger1.write(90);
  finger2.attach(5);  // attaches the servo on pin 9 to the servo object
  finger2.write(90);
  finger3.attach(18);  // attaches the servo on pin 9 to the servo object
  finger3.write(90);
  finger4.attach(19);  // attaches the servo on pin 9 to the servo object
  finger4.write(90);
  finger5.attach(21);  // attaches the servo on pin 9 to the servo object
  finger5.write(90);
}

void loop() {

  finger1.write(110);
  finger2.write(125);
  finger3.write(90);
  finger4.write(140);
  finger5.write(155);

  // finger1.write(95);
  // finger2.write(95);
  // finger3.write(95);
  // finger4.write(95);
  // finger5.write(95);
  
  delay(2000);
  
  finger1.write(90);
  finger2.write(90);
  finger3.write(90);
  finger4.write(90);
  finger5.write(90);
  
  delay(2000);

}
