import cv2
import serial
import time
import numpy as np

# Open serial connection
ser = serial.Serial('COM7', 9600, timeout=1)
time.sleep(2)

# Red laser color threshold (BGR) – adjust if using green or blue laser
lower = np.array([0, 0, 250])
upper = np.array([240, 240, 255])

# Sweep range for calibration
x_angles = range(0, 121, 10)
y_angles = range(30, 101, 10)

# Start camera
cap = cv2.VideoCapture(0)
time.sleep(1)

data = []

print("🟢 Starting servo-laser calibration... Press ESC to abort.")

for y in y_angles:
    for x in x_angles:
        cmd = f"{x},{y}\n"
        ser.write(cmd.encode())
        print(f"Moving to: X={x}°, Y={y}°")
        time.sleep(0.6)

        ret, frame = cap.read()
        if not ret:
            continue

        # Detect laser dot
        blur = cv2.GaussianBlur(frame, (5, 5), 0)
        mask = cv2.inRange(blur, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        laser_found = False
        if contours:
            largest = max(contours, key=cv2.contourArea)
            if cv2.contourArea(largest) > 5:
                M = cv2.moments(largest)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    data.append(((x, y), (cx, cy)))
                    laser_found = True

                    # Draw dot
                    cv2.circle(frame, (cx, cy), 8, (0, 255, 0), -1)
                    cv2.putText(frame, f"({cx}, {cy})", (cx + 10, cy), cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, (0, 255, 0), 2)

        # Overlay info
        status = f"X={x}° Y={y}° | Laser {'FOUND' if laser_found else 'NOT FOUND'}"
        cv2.putText(frame, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0, 255, 0) if laser_found else (0, 0, 255), 2)

        # Show frame
        cv2.imshow("Laser Calibration View", frame)
        if cv2.waitKey(1) == 27:  # ESC to break early
            break

cap.release()
cv2.destroyAllWindows()
ser.close()

# Process results
if not data:
    print("❌ No laser dot detected in any position.")
    exit()

# Get min/max screen positions
left   = min(data, key=lambda d: d[1][0])
right  = max(data, key=lambda d: d[1][0])
top    = min(data, key=lambda d: d[1][1])
bottom = max(data, key=lambda d: d[1][1])

# Final servo angle limits
servoXMin = left[0][0]
servoXMax = right[0][0]
servoYMin = top[0][1]
servoYMax = bottom[0][1]

# Print calibrated limits
print("\n✅ Calibrated Servo Limits Based on Laser Position:")
print(f"servoXMin = {servoXMin}")
print(f"servoXMax = {servoXMax}")
print(f"servoYMin = {servoYMin}")
print(f"servoYMax = {servoYMax}")
