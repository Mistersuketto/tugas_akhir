from ultralytics import YOLO
import cv2
import numpy as np

# Load YOLO model
model = YOLO("best.pt")

# Buka webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Prediksi YOLO pada frame
    results = model.predict(
        source=frame,
        conf=0.25,
        classes=[0, 1, 2, 3, 4, 6],
        verbose=False
    )

    # Ambil hasil deteksi
    for r in results:
        boxes = r.boxes.xyxy.cpu().numpy().astype(int)
        for box in boxes:
            x1, y1, x2, y2 = box[:4]
            roi = frame[y1:y2, x1:x2]

            # Segmentasi HSV pada ROI
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            # Contoh: threshold warna hijau
            lower = np.array([35, 50, 50])
            upper = np.array([85, 255, 255])
            mask = cv2.inRange(hsv, lower, upper)

            # Tampilkan bounding box dan mask
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.imshow("HSV Mask", mask)

    cv2.imshow("YOLO + HSV", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()