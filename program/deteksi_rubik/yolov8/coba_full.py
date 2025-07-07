# from ultralytics import YOLO
# import cv2
# import numpy as np

# # Load YOLO model
# model = YOLO("best.pt")

# # Buka webcam
# cap = cv2.VideoCapture(0)

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Prediksi YOLO pada frame
#     results = model.predict(
#         source=frame,
#         conf=0.25,
#         classes=[0, 1, 2, 3, 4, 6],
#         verbose=False
#     )

#     # Ambil hasil deteksi
#     for r in results:
#         boxes = r.boxes.xyxy.cpu().numpy().astype(int)
#         for box in boxes:
#             x1, y1, x2, y2 = box[:4]
#             roi = frame[y1:y2, x1:x2]

#             # Segmentasi HSV pada ROI
#             hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
#             # Contoh: threshold warna hijau
#             lower = np.array([35, 50, 50])
#             upper = np.array([85, 255, 255])
#             mask = cv2.inRange(hsv, lower, upper)

#             # Temukan kontur pada mask
#             contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#             for cnt in contours:
#                 area = cv2.contourArea(cnt)
#                 if area > 200:  # Filter area kecil
#                     x, y, w, h = cv2.boundingRect(cnt)
#                     # Gambar bounding box pada frame asli (koordinat relatif ROI)
#                     cv2.rectangle(frame, (x1 + x, y1 + y), (x1 + x + w, y1 + y + h), (0, 0, 255), 2)

#             # Tampilkan bounding box dan mask
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
#             cv2.imshow("HSV Mask", mask)

#     cv2.imshow("YOLO + HSV", frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap.release()
from ultralytics import YOLO
import cv2
import numpy as np

# Load YOLO model
model = YOLO("best.pt")

# Buka webcam
cap = cv2.VideoCapture(0)

# Definisikan rentang HSV untuk setiap warna Rubik
# Format: 'NamaWarna': ([lower_hsv], [upper_hsv])
# Catatan: Merah memiliki dua rentang karena melintasi batas HUE 0/179
color_ranges = {
    'Merah': [([0, 120, 70], [10, 255, 255]), ([170, 120, 70], [180, 255, 255])],
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
        # 'classes' bisa dikosongkan jika model hanya mendeteksi 1 jenis objek (misal: "sticker")
        # classes=[0, 1, 2, 3, 4, 6], 
        verbose=False
    )

    # Ambil hasil deteksi
    for r in results:
        boxes = r.boxes.xyxy.cpu().numpy().astype(int)
        for box in boxes:
            x1, y1, x2, y2 = box[:4]
            # Ambil Region of Interest (ROI) dari deteksi YOLO
            roi = frame[y1:y2, x1:x2]

            # Lewati jika ROI kosong
            if roi.size == 0:
                continue

            # Konversi ROI ke HSV color space
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
            # --- Loop untuk setiap warna yang telah didefinisikan ---
            for color_name, ranges in color_ranges.items():
                
                # Buat mask untuk setiap warna
                # Handle kasus khusus untuk warna merah
                if color_name == 'Merah':
                    mask1 = cv2.inRange(hsv, np.array(ranges[0][0]), np.array(ranges[0][1]))
                    mask2 = cv2.inRange(hsv, np.array(ranges[1][0]), np.array(ranges[1][1]))
                    mask = cv2.bitwise_or(mask1, mask2)
                else:
                    mask = cv2.inRange(hsv, np.array(ranges[0][0]), np.array(ranges[0][1]))

                # Temukan kontur pada mask
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area > 100:  # Filter area kecil untuk mengurangi noise
                        x, y, w, h = cv2.boundingRect(cnt)
                        # Gambar bounding box pada frame asli dengan warna yang sesuai
                        # Koordinat harus disesuaikan dengan posisi ROI (x1, y1)
                        cv2.rectangle(frame, (x1 + x, y1 + y), (x1 + x + w, y1 + y + h), drawing_colors_bgr[color_name], 2)
                        # Tambahkan label nama warna
                        cv2.putText(frame, color_name, (x1 + x, y1 + y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, drawing_colors_bgr[color_name], 2)

                # Tampilkan setiap mask warna di jendela yang berbeda
                cv2.imshow(f"Mask - {color_name}", mask)

            # Gambar bounding box hijau dari deteksi YOLO awal
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Deteksi Rubik", frame)
    # Tekan tombol ESC untuk keluar
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()