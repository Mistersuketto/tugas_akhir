import cv2
import numpy as np
from ultralytics import YOLO
import time

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

# Urutan standar untuk algoritma solver
SOLVE_ORDER = ['U', 'R', 'F', 'D', 'L', 'B']

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
    """Menganalisis ROI wajah rubik dan mengembalikan 9 warnanya."""
    face_colors = []
    height, width, _ = face_roi.shape
    cell_h, cell_w = height // 3, width // 3
    
    for i in range(3): # Loop baris
        for j in range(3): # Loop kolom
            x_start, y_start = j * cell_w, i * cell_h
            cell = face_roi[y_start:y_start + cell_h, x_start:x_start + cell_w]
            margin = int(cell_w * 0.2)
            center_cell = cell[margin:-margin, margin:-margin]
            
            if center_cell.size == 0:
                face_colors.append("Unknown"); continue

            hsv_cell = cv2.cvtColor(center_cell, cv2.COLOR_BGR2HSV)
            avg_hsv = cv2.mean(hsv_cell)[:3]
            face_colors.append(get_color_name(avg_hsv))
            
    return face_colors

def draw_status_overlay(frame, state, order):
    """Menggambar status pemindaian di bagian atas layar."""
    y_offset = 30
    font_scale = 0.7
    status_text = "Status: "
    for face in order:
        if face in state:
            status_text += f"[{face} ✓] "
        else:
            status_text += f"[{face}  ] "
    
    cv2.putText(frame, status_text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 
                font_scale, (0, 0, 0), 3) # Outline hitam
    cv2.putText(frame, status_text, (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 
                font_scale, (0, 255, 255), 2) # Teks kuning

# ===================================================================
# LOOP UTAMA
# ===================================================================

cap = cv2.VideoCapture(0)
rubik_state = {}
last_scan_time = 0
FEEDBACK_DURATION_SEC = 2.0

while len(rubik_state) < 6:
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(source=frame, conf=0.7, verbose=False, stream=False)

    if results and len(results[0].boxes) > 0:
        best_detection_idx = results[0].boxes.conf.argmax()
        box = results[0].boxes[best_detection_idx]
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        
        face_roi = frame[y1:y2, x1:x2]

        if face_roi.size > 0:
            face_colors = analyze_face_grid(face_roi)
            center_color = face_colors[4]
            verified_face_notation = center_color_map.get(center_color, "Unknown")

            # Kondisi untuk memindai secara otomatis
            all_colors_known = "Unknown" not in face_colors
            not_yet_scanned = verified_face_notation not in rubik_state

            if all_colors_known and not_yet_scanned:
                kociemba_string = "".join([center_color_map.get(c, '?') for c in face_colors])
                rubik_state[verified_face_notation] = kociemba_string
                last_scan_time = time.time()
                
                print(f"\n--- SISI '{verified_face_notation}' ({center_color}) BERHASIL DISIMPAN ---")
                print(f"Hasil Pindai: {kociemba_string}")

            # Atur umpan balik visual
            time_since_last_scan = time.time() - last_scan_time
            if time_since_last_scan < FEEDBACK_DURATION_SEC:
                # Warna biru sebagai indikator "SAVED"
                box_color = (255, 0, 0)
                label_text = "SAVED!"
            else:
                # Warna hijau sebagai indikator "Ready to Scan"
                box_color = (0, 255, 0)
                label_text = f"Show: {verified_face_notation} ({center_color})"

            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
            cv2.putText(frame, label_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, box_color, 2)
    
    # Gambar status di setiap frame
    draw_status_overlay(frame, rubik_state, SOLVE_ORDER)
    cv2.imshow("Automatic Rubik's Scanner", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# --- SETELAH SEMUA SISI TERPINDAI ---
print("\n=============================================")
print("✅ SEMUA 6 SISI BERHASIL DIPINDAI!")
print("=============================================")

# Susun string final sesuai urutan URFDLB
final_kociemba_string = "".join([rubik_state.get(face, "?"*9) for face in SOLVE_ORDER])

print("STRING FINAL UNTUK SOLVER KOCIEMBA:")
print(final_kociemba_string)

# Tampilkan pesan "SELESAI" di layar selama beberapa detik
while True:
    ret, frame = cap.read()
    if not ret: break
    
    (w, h), _ = cv2.getTextSize("SCAN COMPLETE", cv2.FONT_HERSHEY_TRIPLEX, 3, 5)
    x = frame.shape[1] // 2 - w // 2
    y = frame.shape[0] // 2 + h // 2
    
    cv2.putText(frame, "SCAN COMPLETE", (x, y), cv2.FONT_HERSHEY_TRIPLEX, 3, (0,0,0), 8)
    cv2.putText(frame, "SCAN COMPLETE", (x, y), cv2.FONT_HERSHEY_TRIPLEX, 3, (0,255,0), 5)
    cv2.imshow("Automatic Rubik's Scanner", frame)
    
    if cv2.waitKey(1000): break # Tunggu sebentar lalu keluar

cap.release()
cv2.destroyAllWindows()