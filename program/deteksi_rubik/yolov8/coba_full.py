from ultralytics import YOLO
import cv2
import numpy as np

# Load YOLO model
model = YOLO("best.pt")

# Buka webcam
cap = cv2.VideoCapture(0)

# Definisikan rentang HSV untuk setiap warna Rubik
color_ranges = {
    # --- PERUBAHAN DI SINI ---
    # Rentang Merah disesuaikan dengan nilai BGR(157, 103, 226) -> HSV(167, 103, 226)
    # Kita beri toleransi agar lebih fleksibel terhadap pencahayaan.
    'Merah': [([155, 70, 70], [175, 255, 255])],
    'Oranye': [([11, 120, 70], [25, 255, 255])],
    'Kuning': [([26, 100, 70], [34, 255, 255])],
    'Hijau': [([35, 50, 50], [85, 255, 255])],
    'Biru': [([90, 80, 50], [128, 255, 255])],
    'Putih': [([0, 0, 180], [180, 40, 255])]
}

# Definisikan warna BGR untuk menggambar bounding box
drawing_colors_bgr = {
    'Merah': (0, 0, 255),
    'Oranye': (0, 165, 255),
    'Kuning': (0, 255, 255),
    'Hijau': (0, 255, 0),
    'Biru': (255, 0, 0),
    'Putih': (255, 255, 255)
}


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Prediksi YOLO pada frame
    results = model.predict(
        source=frame,
        conf=0.25,
        verbose=False
    )

    # Ambil hasil deteksi
    for r in results:
        boxes = r.boxes.xyxy.cpu().numpy().astype(int)
        for box in boxes:
            x1, y1, x2, y2 = box[:4]
            roi = frame[y1:y2, x1:x2]

            if roi.size == 0:
                continue

            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
            for color_name, ranges in color_ranges.items():
                
                # --- PERUBAHAN DI SINI ---
                # Logika if/else untuk Merah dihapus karena rentang baru hanya satu blok.
                # Kode ini sekarang berlaku sama untuk semua warna.
                mask = cv2.inRange(hsv, np.array(ranges[0][0]), np.array(ranges[0][1]))

                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area > 100:
                        x, y, w, h = cv2.boundingRect(cnt)
                        cv2.rectangle(frame, (x1 + x, y1 + y), (x1 + x + w, y1 + y + h), drawing_colors_bgr[color_name], 2)
                        cv2.putText(frame, color_name, (x1 + x, y1 + y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, drawing_colors_bgr[color_name], 2)

                cv2.imshow(f"Mask - {color_name}", mask)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Deteksi Rubik", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()