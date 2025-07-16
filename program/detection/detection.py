# detection/detection_module.py

import cv2
import numpy as np
from ultralytics import YOLO
import time

# ===================================================================
# BAGIAN 1: PENGATURAN DAN KONFIGURASI (Tidak ada perubahan)
# ===================================================================

# Variabel konfigurasi tetap di sini agar bisa diakses oleh fungsi
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
SOLVE_ORDER = ['U', 'R', 'F', 'D', 'L', 'B']
FEEDBACK_DURATION_SEC = 2.0


# ===================================================================
# BAGIAN 2: FUNGSI-FUNGSI BANTU (Tidak ada perubahan)
# ===================================================================
# Semua fungsi bantu (get_color_name, analyze_face_grid, dll.) tetap sama.

def get_color_name(hsv_color):
    h, s, v = hsv_color
    for color_name, hsv_ranges in color_ranges.items():
        for hsv_range in hsv_ranges:
            lower, upper = np.array(hsv_range[0]), np.array(hsv_range[1])
            if lower[0] <= h <= upper[0] and lower[1] <= s <= upper[1] and lower[2] <= v <= upper[2]:
                return color_name
    return "Unknown"

def analyze_face_grid(face_roi):
    face_colors = []
    height, width, _ = face_roi.shape
    cell_h, cell_w = height // 3, width // 3
    for i in range(3):
        for j in range(3):
            cell = face_roi[i*cell_h:(i+1)*cell_h, j*cell_w:(j+1)*cell_w]
            margin = int(cell_w * 0.2)
            center_cell = cell[margin:-margin, margin:-margin]
            if center_cell.size == 0:
                face_colors.append("Unknown"); continue
            hsv_cell = cv2.cvtColor(center_cell, cv2.COLOR_BGR2HSV)
            avg_hsv = cv2.mean(hsv_cell)[:3]
            face_colors.append(get_color_name(avg_hsv))
    return face_colors

def draw_text_with_bg(frame, text, pos, font_scale, text_color, bg_color, padding=5):
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, 2)
    x, y = pos
    cv2.rectangle(frame, (x - padding, y + baseline), (x + text_w + padding, y - text_h - padding), bg_color, -1)
    cv2.putText(frame, text, (x, y), font, font_scale, text_color, 2)

def draw_status_overlay(frame, state, order):
    y_offset = 40
    font_scale = 0.7
    status_text = "Status: "
    for face in order:
        status_text += f"[{face} {'✓' if face in state else ' '}] "
    (w, h), _ = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)
    draw_text_with_bg(frame, status_text, (frame.shape[1] // 2 - w // 2, y_offset), font_scale, (255, 255, 0), (0, 0, 0))


# ===================================================================
# BAGIAN 3: FUNGSI UTAMA MODUL DETEKSI ( <-- PERUBAHAN UTAMA DI SINI)
# ===================================================================
def jalankan_proses_deteksi():
    """
    Fungsi utama untuk menjalankan seluruh proses deteksi Rubik.
    Membuka webcam, memindai 6 sisi, lalu mengembalikan string Kociemba.
    @return: String Kociemba jika berhasil, atau None jika proses dibatalkan.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Error: Tidak dapat membuka webcam.")
        return None # <-- PERUBAHAN: Kembalikan None jika gagal

    rubik_state = {}
    last_scan_time = 0
    start_time = time.time()
    print("🚀 Memulai pemindai Rubik otomatis. Tunjukkan setiap sisi ke kamera...")

    while len(rubik_state) < 6:
        ret, frame = cap.read()
        if not ret:
            print("❌ Gagal membaca frame dari webcam.")
            break
        
        results = model.predict(source=frame, conf=0.7, verbose=False, stream=False)
        if results and len(results[0].boxes) > 0:
            box = results[0].boxes.conf.argmax()
            x1, y1, x2, y2 = map(int, results[0].boxes.xyxy[box])
            face_roi = frame[y1:y2, x1:x2]
            if face_roi.size > 0:
                face_colors = analyze_face_grid(face_roi)
                center_color = face_colors[4]
                verified_face_notation = center_color_map.get(center_color, "Unknown")
                all_colors_known = "Unknown" not in face_colors
                not_yet_scanned = verified_face_notation not in rubik_state
                if all_colors_known and not_yet_scanned:
                    kociemba_string = "".join([center_color_map.get(c, '?') for c in face_colors])
                    rubik_state[verified_face_notation] = kociemba_string
                    last_scan_time = time.time()
                    print(f"✔️  Sisi '{verified_face_notation}' ({center_color}) berhasil disimpan.")
                
                time_since_last_scan = time.time() - last_scan_time
                if time_since_last_scan < FEEDBACK_DURATION_SEC:
                    box_color, label_text = ((255, 100, 100), "SAVED!")
                else:
                    box_color, label_text = ((0, 255, 0), f"Show: {verified_face_notation} ({center_color})")
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 3)
                draw_text_with_bg(frame, label_text, (x1, y1 - 10), 0.7, (255,255,255), box_color)

        draw_status_overlay(frame, rubik_state, SOLVE_ORDER)
        cv2.imshow("Automatic Rubik's Scanner", frame)

        if cv2.waitKey(1) & 0xFF == 27: # Tekan ESC untuk keluar
            print("🔴 Proses dihentikan oleh pengguna.")
            cap.release()
            cv2.destroyAllWindows()
            return None # <-- PERUBAHAN: Kembalikan None jika dibatalkan

    # --- Proses Akhir Setelah Semua Sisi Terpindai ---
    end_time = time.time()
    detection_duration_sec = end_time - start_time

    print("\n=============================================")
    print("✅ SEMUA 6 SISI BERHASIL DIPINDAI!")
    print(f"Rubik berhasil dideteksi dalam waktu {detection_duration_sec:.2f} detik")
    print("=============================================")
    
    final_kociemba_string = "".join([rubik_state.get(face, "?"*9) for face in SOLVE_ORDER])
    
    cap.release()
    cv2.destroyAllWindows()
    
    # <-- PERUBAHAN PALING PENTING:
    return final_kociemba_string


# ===================================================================
# BAGIAN 4: BLOK EKSEKUSI (Untuk Testing Mandiri)
# ===================================================================
if __name__ == '__main__':
    # Blok ini hanya akan berjalan jika Anda menjalankan file ini secara langsung
    # (python detection_module.py), bukan saat diimpor oleh main.py.
    print("Menjalankan modul deteksi secara mandiri untuk pengujian...")
    hasil_deteksi = jalankan_proses_deteksi()
    
    if hasil_deteksi:
        print("\nSTRING FINAL YANG DIDETEKSI:")
        print(hasil_deteksi)
    else:
        print("\nTidak ada hasil deteksi atau proses dibatalkan.")