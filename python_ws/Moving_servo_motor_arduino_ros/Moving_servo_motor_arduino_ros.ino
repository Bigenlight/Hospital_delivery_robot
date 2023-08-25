#include <Servo.h>

Servo myservo;
int pos = 0;

void setup() {
  Serial.begin(9600);
  myservo.attach(9); // Use the appropriate pin for your servo
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n'); // Read a string until a newline character

    // Convert the string to an integer
    int targetPosition = input.toInt();
    if (targetPosition >= 0 && targetPosition <= 180) {
      // Move the servo to the target position
      myservo.write(targetPosition);
      Serial.print("Servo moved to ");
      Serial.println(targetPosition);
    } else {
      Serial.println("Invalid position. Please enter a value between 0 and 180.");
    }

    while (Serial.available()) {
      Serial.read(); // Clear any remaining characters in the serial buffer
    }
  }
}
