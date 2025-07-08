import cv2
import numpy as np
from ultralytics import YOLO

# ===================================================================
# PENGATURAN AWAL
# ===================================================================

# Muat model YOLOv8 yang sudah Anda latih
model = YOLO("best.pt")

# Definisikan rentang warna HSV.
# PENTING: Nilai ini mungkin perlu Anda sesuaikan (kalibrasi)
# agar cocok dengan kamera dan kondisi pencahayaan Anda.
color_ranges = {
    'Putih':  [([0, 0, 150], [180, 55, 255])],
    'Kuning': [([22, 90, 100], [35, 255, 255])],
    'Hijau':  [([36, 80, 50], [90, 255, 255])],
    'Biru':   [([91, 80, 50], [128, 255, 255])],
    'Merah':  [([151, 48, 128], [171, 255, 255])],
    'Oranye': [([11, 120, 70], [21, 255, 255])]
}

# Kamus untuk memetakan warna tengah ke notasi sisi Rubik.
# Inilah "kunci jawaban" untuk verifikasi.
# Sesuaikan jika skema warna Rubik Anda berbeda.
center_color_map = {
    'Putih':  'U', # Up
    'Kuning': 'D', # Down
    'Hijau':  'F', # Front
    'Biru':   'B', # Back
    'Merah':  'R', # Right
    'Oranye': 'L'  # Left
}

# ===================================================================
# FUNGSI BANTU
# ===================================================================

def get_color_name(hsv_color):
    """Mendeteksi nama warna dari sebuah nilai HSV rata-rata."""
    h, s, v = hsv_color
    for color_name, hsv_ranges in color_ranges.items():
        for hsv_range in hsv_ranges:
            lower, upper = np.array(hsv_range[0]), np.array(hsv_range[1])
            if lower[0] <= h <= upper[0] and lower[1] <= s <= upper[1] and lower[2] <= v <= upper[2]:
                return color_name
    return "Unknown"

# ===================================================================
# LOOP UTAMA
# ===================================================================

# Buka webcam
cap = cv2.VideoCapture(0)

while True:
    # Baca frame dari webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Lakukan prediksi YOLO pada frame
    results = model.predict(source=frame, conf=0.7, verbose=False)

    # Hanya proses jika ada objek yang terdeteksi
    if results and len(results[0].boxes) > 0:
        # Ambil deteksi dengan kepercayaan tertinggi
        best_detection_idx = results[0].boxes.conf.argmax()
        box = results[0].boxes[best_detection_idx]

        # 1. DAPATKAN PREDIKSI AWAL DARI YOLO
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        yolo_prediction = model.names[int(box.cls[0])]

        # 2. ISOLASI STIKER TENGAH
        face_roi = frame[y1:y2, x1:x2]
        h, w, _ = face_roi.shape
        
        # Ambil area 1/3 di tengah ROI (lokasi stiker tengah)
        cx_start, cx_end = w // 3, w * 2 // 3
        cy_start, cy_end = h // 3, h * 2 // 3
        center_sticker_roi = face_roi[cy_start:cy_end, cx_start:cx_end]
        
        verified_face_notation = "N/A"
        verified_color_name = "N/A"

        if center_sticker_roi.size > 0:
            # 3. ANALISIS WARNA STIKER TENGAH
            hsv_center = cv2.cvtColor(center_sticker_roi, cv2.COLOR_BGR2HSV)
            avg_hsv = cv2.mean(hsv_center)[:3]
            verified_color_name = get_color_name(avg_hsv)
            
            # 4. VERIFIKASI DENGAN 'center_color_map'
            if verified_color_name in center_color_map:
                verified_face_notation = center_color_map[verified_color_name]

        # 5. TAMPILKAN HASIL
        # Gambar kotak deteksi utama
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        
        # Gambar kotak deteksi stiker tengah untuk visualisasi
        cv2.rectangle(frame, (x1 + cx_start, y1 + cy_start), (x1 + cx_end, y1 + cy_end), (255, 0, 0), 2)

        # Siapkan teks label
        label_text = f"YOLO: {yolo_prediction} | Verified: {verified_face_notation} ({verified_color_name})"
        cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


    # Tampilkan frame hasil
    cv2.imshow("Deteksi dan Verifikasi Sisi Rubik", frame)

    # Keluar dari loop jika tombol 'ESC' ditekan
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Bebaskan sumber daya
cap.release()
cv2.destroyAllWindows()