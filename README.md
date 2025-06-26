# 🔧 Laser-Guided Servo Calibration and Tracking System

This project uses a laser pointer, OpenCV, and Arduino to automatically calibrate servo angle limits for a pan-tilt system by detecting the laser dot’s position on a camera feed. It enables precise mapping between screen coordinates and servo angles, making it ideal for auto-tracking, robotic vision, and laser-targeting applications.

## 🎯 Features

- Automatic detection of servo angle limits
- Real-time laser dot tracking using OpenCV
- Serial communication between Python and Arduino
- HSV/BGR-based color detection for laser
- Live camera view with detection overlay
- Plug-and-play calibration for any servo-laser setup

## 🧰 Requirements

### Hardware:
- Arduino Uno or compatible board
- 2 Servo motors (for X and Y axes)
- Laser pointer (mounted on pan-tilt head)
- USB camera (webcam)
- Jumper wires + breadboard (optional)

### Software:
- Python 3.x
- OpenCV (`pip install opencv-python`)
- NumPy
- Arduino IDE

## 🚀 Getting Started

1. **Upload Arduino Code**  
   Open `arduino/laser_servo_control.ino` in Arduino IDE and upload to your board.

2. **Run Python Calibration**  
   Run `python/calibrate_servo_limits.py` to start servo angle sweep and detect laser dot.  
   Adjust HSV/BGR thresholds as needed.

3. **Review Output**  
   The script will calculate and print:
    servoXMin = XX
    servoXMax = XX
    servoYMin = XX
    servoYMax = XX
   
4. **Use Limits in Main Tracking Code**  
Insert these calibrated limits into the main Arduino code for accurate control.



