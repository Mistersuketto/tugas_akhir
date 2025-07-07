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

            # Definisikan rentang HSV untuk setiap warna Rubik
            color_ranges = {
                'U': ([0, 0, 200], [180, 30, 255]),      # Putih
                'R': ([0, 100, 100], [10, 255, 255]),    # Merah
                'F': ([35, 50, 50], [85, 255, 255]),     # Hijau
                'D': ([20, 100, 100], [35, 255, 255]),   # Kuning
                'L': ([10, 100, 100], [20, 255, 255]),   # Orange
                'B': ([100, 100, 100], [130, 255, 255]), # Biru
            }

            detected_piece = None
            for label, (lower, upper) in color_ranges.items():
                lower = np.array(lower, dtype=np.uint8)
                upper = np.array(upper, dtype=np.uint8)
                mask = cv2.inRange(hsv, lower, upper)
                area = cv2.countNonZero(mask)
                if area > 200:  # Threshold area
                    detected_piece = label
                    break

            if detected_piece:
                cv2.putText(frame, detected_piece, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                print(f"Piece terdeteksi: {detected_piece}")

            # Tampilkan bounding box dan mask
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.imshow("HSV Mask", mask)

    cv2.imshow("YOLO + HSV", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()