import cv2
import numpy as np
from ultralytics import YOLO

# ===================================================================
# PENGATURAN AWAL
# ===================================================================

model = YOLO("best.pt")

color_ranges = {
    'Putih':  [([0, 0, 150], [180, 55, 255])],
    'Kuning': [([22, 90, 100], [35, 255, 255])],
    'Hijau':  [([36, 80, 50], [90, 255, 255])],
    'Biru':   [([91, 80, 50], [128, 255, 255])],
    'Merah':  [([151, 48, 128], [171, 255, 255])],
    'Oranye': [([11, 120, 70], [21, 255, 255])]
}

center_color_map = {
    'Putih':  'U', 'Kuning': 'D', 'Hijau':  'F',
    'Biru':   'B', 'Merah':  'R', 'Oranye': 'L'
}

# ===================================================================
# FUNGSI-FUNGSI BANTU
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

def analyze_face_grid(face_roi):
    """
    FUNGSI BARU: Menganalisis ROI wajah rubik, membaginya menjadi grid 3x3,
    dan mengembalikan 9 warnanya beserta gambar visualisasinya.
    """
    face_colors = []
    height, width, _ = face_roi.shape
    cell_h, cell_w = height // 3, width // 3
    
    analyzed_roi = face_roi.copy()
    
    for i in range(3): # Loop baris
        for j in range(3): # Loop kolom
            x_start, y_start = j * cell_w, i * cell_h
            cell = face_roi[y_start:y_start + cell_h, x_start:x_start + cell_w]

            margin = int(cell_w * 0.2)
            center_cell = cell[margin:-margin, margin:-margin]
            
            if center_cell.size == 0:
                face_colors.append("Unknown")
                continue

            hsv_cell = cv2.cvtColor(center_cell, cv2.COLOR_BGR2HSV)
            avg_hsv = cv2.mean(hsv_cell)[:3]
            color_name = get_color_name(avg_hsv)
            face_colors.append(color_name)
            
            # Gambar visualisasi pada jendela analisis
            cv2.rectangle(analyzed_roi, (x_start, y_start), (x_start + cell_w, y_start + cell_h), (0,0,0), 1)
            cv2.putText(analyzed_roi, color_name[0], (x_start + int(cell_w*0.4), y_start + int(cell_h*0.6)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            
    return face_colors, analyzed_roi

# ===================================================================
# LOOP UTAMA
# ===================================================================

cap = cv2.VideoCapture(0)
rubik_state = {}  # Variabel untuk menyimpan state semua sisi

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(source=frame, conf=0.7, verbose=False)

    if results and len(results[0].boxes) > 0:
        best_detection_idx = results[0].boxes.conf.argmax()
        box = results[0].boxes[best_detection_idx]

        x1, y1, x2, y2 = map(int, box.xyxy[0])
        face_roi = frame[y1:y2, x1:x2]

        if face_roi.size > 0:
            # 1. ANALISIS GRID 3X3 PADA SISI YANG TERDETEKSI
            face_colors, analyzed_face = analyze_face_grid(face_roi)
            
            # Tampilkan jendela analisis secara real-time
            cv2.imshow("Analisis Grid 3x3", analyzed_face)

            # 2. VERIFIKASI SISI BERDASARKAN WARNA TENGAH DARI HASIL ANALISIS
            # Stiker tengah adalah elemen ke-5 (indeks 4)
            center_color = face_colors[4]
            verified_face_notation = center_color_map.get(center_color, "Unknown")
            
            # 3. TAMPILKAN HASIL VERIFIKASI DI JENDELA UTAMA
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label_text = f"Sisi Terdeteksi: {verified_face_notation} ({center_color})"
            cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Tampilkan frame utama
    cv2.imshow("Deteksi Rubik", frame)

    # 4. SIMPAN STATE SAAT TOMBOL 's' DITEKAN
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        # Pastikan ada sisi yang terverifikasi sebelum menyimpan
        if 'face_colors' in locals() and verified_face_notation != "Unknown":
            # Konversi daftar warna menjadi string notasi Kociemba
            kociemba_string = "".join([center_color_map.get(c, '?')[0] for c in face_colors])
            rubik_state[verified_face_notation] = kociemba_string
            
            print(f"\n--- SISI '{verified_face_notation}' ({center_color}) BERHASIL DISIMPAN ---")
            print(f"Hasil Pindai: {face_colors}")
            print(f"String Kociemba: {kociemba_string}")
            print("---------------------------------")
            print("State Rubik Saat Ini:")
            for face, state_str in sorted(rubik_state.items()):
                print(f"  {face}: {state_str}")

    # Keluar dari loop jika tombol 'ESC' ditekan
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()