#include <Servo.h>

Servo servoX;
Servo servoY;

void setup() {
  Serial.begin(9600);      // Start serial communication
  servoX.attach(9);        // Attach X-axis servo to pin 9
  servoY.attach(10);       // Attach Y-axis servo to pin 10

  // Optional: Move to center at startup
  servoX.write(90);
  servoY.write(90);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');

    int commaIndex = input.indexOf(',');
    if (commaIndex > 0 && commaIndex < input.length() - 1) {
      int angleX = input.substring(0, commaIndex).toInt();
      int angleY = input.substring(commaIndex + 1).toInt();

      angleX = constrain(angleX, 0, 180);
      angleY = constrain(angleY, 0, 180);

      servoX.write(angleX);
      servoY.write(angleY);

      // Optional: Acknowledge movement
      Serial.print("Moved to: ");
      Serial.print(angleX);
      Serial.print(", ");
      Serial.println(angleY);
    }
  }
}
