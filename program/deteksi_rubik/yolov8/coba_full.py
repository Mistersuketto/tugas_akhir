from ultralytics import YOLO
import cv2
import numpy as np

# =====================================================================================
# PENGATURAN AWAL
# =====================================================================================

# Muat model YOLOv8 segmentasi yang sudah kamu latih
# Pastikan file 'best.pt' ada di folder yang sama
model = YOLO("best.pt")

# Definisikan rentang warna HSV (SANGAT PENTING untuk dikalibrasi ulang!)
# Gunakan skrip kalibrasi untuk mendapatkan nilai yang akurat sesuai kameramu
color_ranges = {
    # Format: 'NAMA_WARNA': [([H_min, S_min, V_min], [H_max, S_max, V_max])]
    'Putih':  [([0, 0, 180], [180, 40, 255])],
    'Kuning': [([22, 90, 100], [38, 255, 255])],
    'Hijau':  [([40, 80, 50], [90, 255, 255])],
    'Biru':   [([95, 80, 50], [128, 255, 255])],
    'Merah':  [([0, 120, 70], [10, 255, 255]), ([170, 120, 70], [180, 255, 255])], # Merah punya 2 rentang
    'Oranye': [([11, 120, 70], [21, 255, 255])]
}

# Mapping nama warna ke notasi Kociemba (U, R, F, D, L, B)
# Sesuaikan 'center_color_map' dengan warna tengah dari setiap sisi di Rubik-mu
# Contoh: Jika sisi ATAS (Up) rubikmu stiker tengahnya PUTIH, maka 'Putih': 'U'
center_color_map = {
    'Putih':  'U',
    'Hijau':  'F',
    'Kuning': 'D',
    'Biru':   'B',
    'Merah':  'R',
    'Oranye': 'L'
}

# =====================================================================================
# FUNGSI-FUNGSI BANTU
# =====================================================================================

def get_color_name(hsv_color):
    """Mendeteksi nama warna dari sebuah nilai HSV."""
    h, s, v = hsv_color
    for color_name, hsv_ranges in color_ranges.items():
        for hsv_range in hsv_ranges:
            lower, upper = np.array(hsv_range[0]), np.array(hsv_range[1])
            if lower[0] <= h <= upper[0] and lower[1] <= s <= upper[1] and lower[2] <= v <= upper[2]:
                return color_name
    return "N/A" # Tidak terdeteksi

def get_face_colors(warped_face):
    """Menganalisis gambar wajah rubik yang sudah diluruskan dan mengembalikan 9 warnanya."""
    face_colors = []
    cell_size = warped_face.shape[0] // 3
    
    for i in range(3): # Loop baris (row)
        for j in range(3): # Loop kolom (column)
            # Ambil satu sel dari grid 3x3
            x_start, y_start = j * cell_size, i * cell_size
            cell = warped_face[y_start:y_start + cell_size, x_start:x_start + cell_size]

            # Ambil area tengah dari sel untuk menghindari pinggiran
            margin = int(cell_size * 0.2)
            center_cell = cell[margin:-margin, margin:-margin]
            
            if center_cell.size == 0:
                face_colors.append("N/A")
                continue

            # Konversi ke HSV dan hitung nilai rata-rata
            hsv_cell = cv2.cvtColor(center_cell, cv2.COLOR_BGR2HSV)
            avg_hsv = cv2.mean(hsv_cell)[:3]
            
            # Dapatkan nama warna dari nilai HSV rata-rata
            color_name = get_color_name(avg_hsv)
            face_colors.append(color_name)
            
            # Tulis nama warna di sel untuk visualisasi
            cv2.putText(warped_face, color_name[0], (x_start + cell_size // 3, y_start + cell_size // 2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
    return face_colors, warped_face

def order_points(pts):
    """Mengurutkan 4 titik dari masker: atas-kiri, atas-kanan, bawah-kanan, bawah-kiri."""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)] # atas-kiri
    rect[2] = pts[np.argmax(s)] # bawah-kanan
    
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)] # atas-kanan
    rect[3] = pts[np.argmax(diff)] # bawah-kiri
    
    return rect

# =====================================================================================
# LOOP UTAMA
# =====================================================================================

cap = cv2.VideoCapture(0)
rubik_state = {} # Dictionary untuk menyimpan state semua sisi

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Lakukan prediksi dengan model YOLO
    results = model.predict(source=frame, conf=0.6, verbose=False)

    # Hanya proses jika ada deteksi
    if results and results[0].masks:
        # Ambil deteksi dengan kepercayaan tertinggi
        best_detection_idx = results[0].boxes.conf.argmax()
        
        # Dapatkan informasi dari deteksi terbaik
        mask = results[0].masks[best_detection_idx]
        class_id = int(results[0].boxes.cls[best_detection_idx])
        class_name = model.names[class_id] # Contoh: 'atas', 'depan', dll.

        # Gambar masker segmentasi pada frame asli
        mask_coords = mask.xy[0]
        cv2.polylines(frame, [np.int32(mask_coords)], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(frame, class_name, (int(mask_coords[0][0]), int(mask_coords[0][1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # 1. Luruskan Perspektif
        # Tentukan ukuran gambar hasil warp
        width, height = 300, 300
        # Urutkan titik-titik sudut masker
        src_pts = order_points(mask_coords)
        dst_pts = np.array([[0, 0], [width-1, 0], [width-1, height-1], [0, height-1]], dtype="float32")
        
        # Dapatkan matrix transformasi dan lakukan warp
        M = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(frame, M, (width, height))

        # 2. Analisis Warna Grid 3x3
        face_colors, visualized_warped = get_face_colors(warped)
        
        # 3. Tampilkan Hasil
        # Tampilkan gambar yang sudah diluruskan dan dianalisis
        cv2.imshow("Sisi Terdeteksi (Warped & Analyzed)", visualized_warped)

        # Cetak hasil ke konsol saat tombol 's' ditekan
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            center_color = face_colors[4] # Warna tengah (piece ke-5)
            if center_color in center_color_map:
                face_notation = center_color_map[center_color]
                kociemba_string = "".join([center_color_map.get(c, '?')[0] for c in face_colors])
                
                rubik_state[face_notation] = kociemba_string
                
                print(f"\n--- SISI '{class_name.upper()}' ({face_notation}) DISIMPAN ---")
                print(f"Hasil Pindai: {face_colors}")
                print(f"String Kociemba: {kociemba_string}")
                print("---------------------------------")
                print("State Rubik Saat Ini:")
                for face, state_str in rubik_state.items():
                    print(f"  {face}: {state_str}")

    cv2.imshow("Deteksi Rubik", frame)
    if cv2.waitKey(1) & 0xFF == 27: # Keluar dengan tombol ESC
        break

cap.release()
cv2.destroyAllWindows()