import cv2
import numpy as np
from ultralytics import YOLO
import time
import os

# ===================================================================
# BAGIAN 1: PENGATURAN DAN KONFIGURASI GLOBAL
# ===================================================================
# Variabel-variabel di bawah ini digunakan di seluruh modul untuk
# konsistensi dan kemudahan dalam mengubah pengaturan.

# Membuat path absolut ke file model YOLO. Ini memastikan model dapat
# ditemukan tidak peduli dari mana skrip ini dijalankan.
model_path = os.path.join(os.path.dirname(__file__), "best.pt")
model = YOLO(model_path) # Memuat model YOLO yang sudah dilatih.

# Mendefinisikan rentang warna dalam format HSV (Hue, Saturation, Value).
# Setiap warna memiliki rentang nilai [lower_bound, upper_bound].
color_ranges = {
    'Biru':   [([89, 80, 50], [109, 255, 255])],
    'Putih':  [([91, 0, 100], [111, 65, 255])],
    'Oranye': [([3, 100, 70], [24, 255, 255])],
    'Kuning': [([25, 155, 125], [37, 255, 255])],
    'Hijau':  [([40, 80, 50], [55, 255, 255])],
    'Merah':  [([149, 48, 128], [169, 255, 255])]
}

# Memetakan nama warna ke notasi standar Kociemba (U, D, F, B, R, L).
# Ini digunakan untuk mengidentifikasi sisi berdasarkan warna tengahnya.
center_color_map = {
    'Putih':  'U', 'Kuning': 'D', 'Hijau':  'F',
    'Biru':   'B', 'Merah':  'R', 'Oranye': 'L'
}

# Menentukan urutan standar untuk menyusun string Kociemba final.
solve_order = ['U', 'R', 'F', 'D', 'L', 'B']

# Durasi (dalam detik) untuk menampilkan feedback "SAVED!" setelah sisi berhasil dipindai.
feedback_duration_sec = 1.0


# ===================================================================
# BAGIAN 2: FUNGSI-FUNGSI BANTU
# ===================================================================

def get_color_name(hsv_color):
    """
    Mengidentifikasi nama warna (e.g., 'Merah', 'Biru') dari nilai HSV yang diberikan.
    Fungsi ini membandingkan nilai HSV input dengan rentang warna yang telah didefinisikan
    di `color_ranges`.

    @param hsv_color: Tuple atau list berisi nilai (Hue, Saturation, Value).
    @return: String nama warna yang cocok, atau "Unknown" jika tidak ada yang cocok.
    """
    # Ekstrak nilai Hue, Saturation, dan Value dari input
    h, s, v = hsv_color

    # Iterasi melalui setiap warna dan rentang HSV-nya yang ada di 'color_ranges'
    for color_name, hsv_ranges in color_ranges.items():
        for hsv_range in hsv_ranges:
            # Tentukan batas bawah dan batas atas dari rentang warna
            lower_bound, upper_bound = np.array(hsv_range[0]), np.array(hsv_range[1])

            # Periksa apakah nilai H, S, dan V dari input berada di dalam rentang saat ini
            if lower_bound[0] <= h <= upper_bound[0] and lower_bound[1] <= s <= upper_bound[1] and lower_bound[2] <= v <= upper_bound[2]:
                # Jika cocok, kembalikan nama warnanya dan hentikan fungsi
                return color_name
            
    # Jika loop selesai tanpa menemukan warna yang cocok, kembalikan "Unknown"
    return "Unknown"

# -------------------------------------------------------------------

def analyze_face_grid(face_roi):
    """
    Menganalisis gambar satu sisi Rubik (ROI) dan mengidentifikasi warna dari 9 stiker.
    Fungsi ini membagi gambar ROI menjadi grid 3x3, lalu mengambil warna rata-rata dari
    bagian tengah setiap sel untuk menentukan warna stiker.

    @param face_roi: Gambar (frame) dari satu sisi Rubik yang sudah dipotong (Region of Interest).
    @return: List berisi 9 string nama warna, sesuai urutan grid dari kiri-atas ke kanan-bawah.
    """
    face_colors = [] # List untuk menyimpan hasil identifikasi 9 warna stiker
    height, width, _ = face_roi.shape

    # Hitung tinggi dan lebar setiap sel dalam grid 3x3
    cell_height, cell_width = height // 3, width // 3

    # Iterasi untuk setiap baris (i) dan kolom (j) pada grid 3x3
    for i in range(3):
        for j in range(3):
            # Potong gambar untuk mendapatkan satu sel dari grid
            cell = face_roi[i*cell_height:(i+1)*cell_height, j*cell_width:(j+1)*cell_width]

            # Tentukan margin untuk mengambil area tengah sel. Ini untuk menghindari
            # noise atau warna dari stiker tetangga di bagian tepi.
            margin = int(cell_width * 0.2)
            center_cell = cell[margin:-margin, margin:-margin]

            # Jika sel tengah kosong (karena ROI sangat kecil), anggap tidak diketahui
            if center_cell.size == 0:
                face_colors.append("Unknown")
                continue

            # Konversi BGR ke HSV untuk deteksi warna yang lebih baik
            hsv_cell = cv2.cvtColor(center_cell, cv2.COLOR_BGR2HSV)

            # Hitung nilai rata-rata HSV dari area tengah sel
            avg_hsv = cv2.mean(hsv_cell)[:3]

            # Terjemahkan nilai HSV rata-rata menjadi nama warna
            face_colors.append(get_color_name(avg_hsv))

    return face_colors

# -------------------------------------------------------------------

def draw_text_with_bg(frame, text, pos, font_scale, text_color, bg_color, padding=5):
    """
    Menggambar teks pada frame dengan latar belakang berwarna agar mudah dibaca.
    
    @param frame: Frame video (gambar) tempat teks akan digambar.
    @param text: String teks yang akan ditampilkan.
    @param pos: Tuple (x, y) koordinat untuk posisi teks (pojok kiri atas).
    @param font_scale: Ukuran skala font.
    @param text_color: Tuple warna (B, G, R) untuk teks.
    @param bg_color: Tuple warna (B, G, R) untuk latar belakang.
    @param padding: Jarak (pixel) antara teks dan tepi latar belakang.
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Hitung ukuran lebar dan tinggi teks untuk membuat latar belakang yang pas
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, 2)
    x, y = pos

    # Gambar persegi panjang sebagai latar belakang
    cv2.rectangle(frame, (x - padding, y + baseline), (x + text_width + padding, y - text_height - padding), bg_color, -1)

    # Tulis teks di atas latar belakang yang sudah digambar
    cv2.putText(frame, text, (x, y), font, font_scale, text_color, 2)

# -------------------------------------------------------------------

def draw_status_overlay(frame, state, order):
    """
    Menampilkan status pemindaian (sisi mana yang sudah dan belum) di bagian atas frame.

    Contoh: [U ✓] [R  ] [F ✓] ...

    @param frame: Frame video (gambar) untuk menampilkan status.
    @param state: Dictionary yang menyimpan status pemindaian (e.g., {'U': 'UUU...'})
    @param order: List yang menentukan urutan tampilan status (e.g., solve_order).
    """
    y_offset = 40
    font_scale = 0.7
    status_text = "Status: "

    # Bangun string status dengan iterasi sesuai urutan 'solve_order'
    for face in order:
        # Cek jika 'face' sudah ada di 'state', tampilkan '✓', jika tidak, tampilkan spasi
        status_text += f"[{face} {'✓' if face in state else ' '}] "

    # Hitung lebar total teks status untuk memposisikannya di tengah
    (status_width, _), _ = cv2.getTextSize(status_text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)

    # Posisikan dan gambar teks status di tengah atas layar
    draw_text_with_bg(frame, status_text, (frame.shape[1] // 2 - status_width // 2, y_offset), font_scale, (255, 255, 0), (0, 0, 0))


# ===================================================================
# BAGIAN 3: FUNGSI UTAMA MODUL DETEKSI
# ===================================================================

def jalankan_proses_deteksi():
    """
    Fungsi utama untuk menjalankan seluruh proses deteksi Rubik.

    Membuka webcam, memindai 6 sisi secara berurutan, lalu mengembalikan
    string Kociemba yang siap digunakan untuk solver.

    @return: String Kociemba lengkap jika semua 6 sisi berhasil dipindai.
             Mengembalikan `None` jika proses dibatalkan oleh pengguna (menekan ESC)
             atau jika webcam tidak dapat dibuka.
    """
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print("❌ Error: Tidak dapat membuka webcam.")
        return None

    rubik_state = {} # Dictionary untuk menyimpan string Kociemba per sisi (e.g., {'U': 'UUU...'})
    last_scan_time = 0
    start_time = time.time()
    print("🚀 Memulai pemindai Rubik otomatis. Tunjukkan setiap sisi ke kamera...")

    # Loop utama, akan terus berjalan sampai 6 sisi berhasil dipindai
    while len(rubik_state) < 6:
        ret, frame = cap.read() # Baca satu frame dari webcam
        if not ret:
            print("❌ Gagal membaca frame dari webcam.")
            break

        # Lakukan prediksi dengan model YOLO untuk mendeteksi sisi Rubik
        results = model.predict(source=frame, conf=0.7, verbose=False, stream=False)

        # Jika model berhasil mendeteksi objek
        if results and len(results[0].boxes) > 0:
            # Ambil bounding box dari deteksi dengan confidence (keyakinan) tertinggi
            box = results[0].boxes.conf.argmax()
            x1, y1, x2, y2 = map(int, results[0].boxes.xyxy[box])

            # Potong frame untuk mendapatkan gambar sisi Rubik saja (Region of Interest)
            face_roi = frame[y1:y2, x1:x2]

            if face_roi.size > 0:
                # Analisis ROI untuk mendapatkan 9 warna stiker
                face_colors = analyze_face_grid(face_roi)
                # Warna tengah (indeks 4) menentukan notasi sisi (U, R, F, dll.)
                center_color = face_colors[4]
                verified_face_notation = center_color_map.get(center_color, "Unknown")

                # ---- Logika untuk memvalidasi dan menyimpan pemindaian ----
                # 1. Pastikan semua 9 stiker teridentifikasi (tidak ada "Unknown")
                all_colors_known = "Unknown" not in face_colors
                # 2. Pastikan sisi ini belum pernah dipindai sebelumnya
                not_yet_scanned = verified_face_notation not in rubik_state

                # Simpan hanya jika semua warna terdeteksi dan sisi belum pernah dipindai
                if all_colors_known and not_yet_scanned:
                    # Gabungkan notasi 9 warna menjadi satu string (e.g., "UUURRRFFF")
                    kociemba_string = "".join([center_color_map.get(c, '?') for c in face_colors])
                    # Simpan string tersebut ke dalam state utama
                    rubik_state[verified_face_notation] = kociemba_string
                    # Catat waktu pemindaian berhasil untuk feedback visual
                    last_scan_time = time.time()
                    print(f"✔️  Sisi '{verified_face_notation}' ({center_color}) berhasil disimpan.")

                # ---- Berikan feedback visual kepada pengguna ----
                time_since_last_scan = time.time() - last_scan_time
                # Jika pemindaian baru saja berhasil, tampilkan "SAVED!" selama beberapa detik
                if time_since_last_scan < feedback_duration_sec:
                    box_color, label_text = ((255, 100, 100), "SAVED!")
                else:
                    # Jika tidak, tampilkan instruksi sisi apa yang sedang dilihat kamera
                    box_color, label_text = ((0, 255, 0), f"Show: {verified_face_notation} ({center_color})")

                # Gambar bounding box dan labelnya pada frame
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 3)
                draw_text_with_bg(frame, label_text, (x1, y1 - 10), 0.7, (255, 255, 255), box_color)

        # Gambar status pemindaian di bagian atas frame
        draw_status_overlay(frame, rubik_state, solve_order)
        # Tampilkan frame yang sudah diproses ke pengguna
        cv2.imshow("Automatic Rubik's Scanner", frame)

        # Periksa apakah pengguna menekan tombol ESC (kode ASCII 27) untuk keluar
        if cv2.waitKey(1) & 0xFF == 27:
            print("🔴 Proses dihentikan oleh pengguna.")
            cap.release()
            cv2.destroyAllWindows()
            return None

    # --- Proses Akhir Setelah Semua Sisi Terpindai ---
    end_time = time.time()
    detection_duration_sec = end_time - start_time

    print("\n=============================================")
    print("✅ SEMUA 6 SISI BERHASIL DIPINDAI!")
    print(f"Rubik berhasil dideteksi dalam waktu {detection_duration_sec:.2f} detik")
    print("=============================================")

    # Susun string Kociemba final dengan menggabungkan hasil dari setiap sisi
    # sesuai dengan urutan standar 'solve_order'.
    final_kociemba_string = "".join([rubik_state.get(face, "?"*9) for face in solve_order])

    # Lepaskan webcam dan tutup semua jendela OpenCV
    cap.release()
    cv2.destroyAllWindows()

    return final_kociemba_string


# ===================================================================
# BAGIAN 4: BLOK EKSEKUSI (Untuk Testing Mandiri)
# ===================================================================
if __name__ == '__main__':
    """
    Blok ini hanya akan berjalan jika Anda menjalankan file ini secara langsung
    (misalnya, dengan `python detection/detection.py`).
    Ini berguna untuk menguji fungsionalitas modul deteksi secara terpisah
    tanpa perlu menjalankan aplikasi utama (`main.py`).
    """
    print("Menjalankan modul deteksi secara mandiri untuk pengujian...")
    hasil_deteksi = jalankan_proses_deteksi()

    if hasil_deteksi:
        print("\nSTRING FINAL YANG DIDETEKSI (KOCIEMBA):")
        print(hasil_deteksi)
    else:
        print("\nTidak ada hasil deteksi atau proses dibatalkan.")