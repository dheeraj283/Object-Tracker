import cv2
import cv2.aruco as aruco
import serial
import time

# === SERIAL SETUP ===
arduino = serial.Serial('COM7', 9600)
time.sleep(2)

# === CAMERA SETUP ===
cap = cv2.VideoCapture(0)
frame_width = 640
frame_height = 480

cap.set(3, frame_width)
cap.set(4, frame_height)

# === LOAD ARUCO DICTIONARY ===
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)
parameters = aruco.DetectorParameters()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detector = aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, _ = detector.detectMarkers(gray)

    if ids is not None:
        for corner in corners:
            pts = corner[0]
            cx = int(pts[:, 0].mean())
            cy = int(pts[:, 1].mean())

            # Draw marker and centroid
            cv2.polylines(frame, [pts.astype(int)], True, (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 255), -1)
            cv2.putText(frame, f"X: {cx} Y: {cy}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            # Send both coordinates
            arduino.write(f"{cx},{cy}\n".encode())
            break

    cv2.imshow("Aruco Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
