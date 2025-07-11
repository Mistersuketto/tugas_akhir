# =============================================================================
# PEMINDIA OTOMATIS RUBIK'S CUBE
# -----------------------------------------------------------------------------
# Deskripsi:
# Program ini menggunakan model deteksi objek YOLOv8 untuk menemukan wajah
# Rubik's Cube dari webcam. Setelah wajah terdeteksi, program akan
# menganalisis grid 3x3 untuk mengidentifikasi 9 warna stiker.
# Program secara otomatis akan memindai ke-6 sisi kubus dan menyusun
# sebuah string notasi final yang kompatibel dengan algoritma solver
# seperti Kociemba.
#
# Dependencies: ultralytics, opencv-python, numpy
# =============================================================================

import cv2
import numpy as np
from ultralytics import YOLO
import time

# ===================================================================
# BAGIAN 1: PENGATURAN DAN KONFIGURASI AWAL
# ===================================================================

# Muat model deteksi YOLOv8 yang sudah Anda latih.
model = YOLO("best.pt")

# Definisikan rentang warna dalam format HSV (Hue, Saturation, Value).
color_ranges = {
    'Putih':  [([0, 0, 150], [180, 55, 255])],
    'Kuning': [([22, 90, 100], [35, 255, 255])],
    'Hijau':  [([36, 80, 50], [90, 255, 255])],
    'Biru':   [([91, 80, 50], [128, 255, 255])],
    'Merah':  [([151, 48, 128], [171, 255, 255])],
    'Oranye': [([11, 120, 70], [21, 255, 255])]
}

# Kamus untuk menerjemahkan warna tengah menjadi notasi sisi standar (U, R, F, D, L, B).
center_color_map = {
    'Putih':  'U', 'Kuning': 'D', 'Hijau':  'F',
    'Biru':   'B', 'Merah':  'R', 'Oranye': 'L'
}

# Urutan standar yang diperlukan oleh banyak solver.
SOLVE_ORDER = ['U', 'R', 'F', 'D', 'L', 'B']

# Durasi umpan balik visual setelah pemindaian berhasil (dalam detik).
FEEDBACK_DURATION_SEC = 2.0

# ===================================================================
# BAGIAN 2: FUNGSI-FUNGSI BANTU (HELPER FUNCTIONS)
# ===================================================================

def get_color_name(hsv_color):
    """
    Mendeteksi nama warna dari sebuah nilai HSV rata-rata.
    @param hsv_color: Tuple berisi nilai (H, S, V) dari warna.
    @return: String nama warna (misal: 'Putih') atau 'Unknown' jika tidak ditemukan.
    """
    h, s, v = hsv_color
    for color_name, hsv_ranges in color_ranges.items():
        for hsv_range in hsv_ranges:
            lower, upper = np.array(hsv_range[0]), np.array(hsv_range[1])
            if lower[0] <= h <= upper[0] and lower[1] <= s <= upper[1] and lower[2] <= v <= upper[2]:
                return color_name
    return "Unknown"


def analyze_face_grid(face_roi):
    """
    Menganalisis potongan gambar wajah Rubik (ROI), membaginya menjadi grid 3x3,
    dan mendeteksi warna di setiap sel.
    @param face_roi: Gambar (numpy array) dari wajah Rubik yang telah dipotong.
    @return: List berisi 9 nama warna yang terdeteksi.
    """
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
    """
    Menggambar teks dengan latar belakang agar mudah dibaca.
    @param frame: Frame video untuk digambari.
    @param text: Teks yang ingin ditampilkan.
    @param pos: Posisi (x, y) dari teks.
    @param font_scale: Ukuran font.
    @param text_color: Warna teks (B, G, R).
    @param bg_color: Warna latar belakang (B, G, R).
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, 2)
    x, y = pos
    cv2.rectangle(frame, (x - padding, y + baseline), (x + text_w + padding, y - text_h - padding), bg_color, -1)
    cv2.putText(frame, text, (x, y), font, font_scale, text_color, 2)


def draw_status_overlay(frame, state, order):
    """Menggambar status pemindaian di bagian atas layar."""
    y_offset = 40
    font_scale = 0.7
    status_text = "Status: "
    for face in order:
        status_text += f"[{face} {'✓' if face in state else ' '}] "
    
    (w, h), _ = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)
    draw_text_with_bg(frame, status_text, (frame.shape[1] // 2 - w // 2, y_offset), font_scale, (255, 255, 0), (0, 0, 0))


# ===================================================================
# BAGIAN 3: LOOP UTAMA PROGRAM
# ===================================================================

# Inisialisasi webcam dan variabel state
cap = cv2.VideoCapture(0)
rubik_state = {}
last_scan_time = 0

# Catat waktu mulai untuk menghitung durasi total
start_time = time.time()
print("🚀 Memulai pemindai Rubik otomatis. Tunjukkan setiap sisi ke kamera...")

# Loop utama akan terus berjalan hingga 6 sisi berhasil dipindai
while len(rubik_state) < 6:
    ret, frame = cap.read()
    if not ret:
        print("❌ Gagal membaca frame dari webcam.")
        break

    # Lakukan prediksi YOLO untuk menemukan wajah Rubik
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

            # Atur umpan balik visual untuk pengguna
            time_since_last_scan = time.time() - last_scan_time
            if time_since_last_scan < FEEDBACK_DURATION_SEC:
                box_color = (255, 100, 100) # Biru muda untuk "SAVED"
                label_text = "SAVED!"
            else:
                box_color = (0, 255, 0) # Hijau untuk "Ready to Scan"
                label_text = f"Show: {verified_face_notation} ({center_color})"
            
            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 3)
            draw_text_with_bg(frame, label_text, (x1, y1 - 10), 0.7, (255,255,255), box_color)

    # Tampilkan status pemindaian di setiap frame
    draw_status_overlay(frame, rubik_state, SOLVE_ORDER)
    cv2.imshow("Automatic Rubik's Scanner", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        print("🔴 Proses dihentikan oleh pengguna.")
        break

# ===================================================================
# BAGIAN 4: PROSES AKHIR SETELAH SEMUA SISI TERPINDAI
# ===================================================================

# Hitung durasi total pemindaian
end_time = time.time()
detection_duration_sec = end_time - start_time
detection_duration_ms = detection_duration_sec * 1000

# Cetak rangkuman hasil ke konsol
print("\n=============================================")
# Hanya cetak jika proses selesai, bukan karena dihentikan pengguna
if len(rubik_state) == 6:
    print("✅ SEMUA 6 SISI BERHASIL DIPINDAI!")
    print(f"Rubik berhasil dideteksi dalam waktu {detection_duration_ms:.0f} ms")
    print("=============================================")
    
    # Susun string notasi final sesuai urutan URFDLB
    final_kociemba_string = "".join([rubik_state.get(face, "?"*9) for face in SOLVE_ORDER])
    
    print("STRING FINAL UNTUK SOLVER KOCIEMBA:")
    print(final_kociemba_string)

# Bebaskan semua sumber daya
cap.release()
cv2.destroyAllWindows()
print("\nProgram selesai. Sampai jumpa! 👋")