#include <Servo.h>

Servo servoX;
Servo servoY;

const int frameWidth = 640;
const int frameHeight = 480;

// ✅ Separate range limits for X and Y axes from caliberation
const int servoXMin = 40;  // Left limit
const int servoXMax = 120; // Right limit

const int servoYMin = 30;  // Top limit
const int servoYMax = 90; // Bottom limit

float xPos = (servoXMax+servoXMin)/2, yPos = (servoYMax+servoYMin)/2;
float targetX = xPos, targetY = yPos;

const float smoothFactor = 0.1;

void setup() {
  Serial.begin(9600);
  servoX.attach(9);
  servoY.attach(10);
  servoX.write(xPos);
  servoY.write(yPos);
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');

    int commaIndex = input.indexOf(',');
    if (commaIndex > 0 && commaIndex < input.length() - 1) {
      int x = input.substring(0, commaIndex).toInt();
      int y = input.substring(commaIndex + 1).toInt();

      targetX = map(x, 0, frameWidth, servoXMin, servoXMax);
      targetX = constrain(targetX, servoXMin, servoXMax);

      targetY = map(y, 0, frameHeight, servoYMin, servoYMax);
      targetY = constrain(targetY, servoYMin, servoYMax);
    }
  }

  xPos += (targetX - xPos) * smoothFactor;
  yPos += (targetY - yPos) * smoothFactor;

  servoX.write(180 - int(xPos));  // Invert if needed
  servoY.write(int(yPos));

  delay(20);
}
