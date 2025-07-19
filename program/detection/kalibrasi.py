import cv2
import numpy as np
import pandas as pd
from datetime import datetime

# --- Variabel Global ---
jumlah_klik = 0
batas_maksimal = 200
data_terkumpul = [] # List untuk menampung semua data

def mouse_callback(event, x, y, flags, param):
    # Gunakan variabel global
    global jumlah_klik
    global data_terkumpul

    # Proses hanya jika event adalah klik kiri dan batas belum tercapai
    if event == cv2.EVENT_LBUTTONDOWN:
        if jumlah_klik < batas_maksimal:
            # Tambah penghitung klik
            jumlah_klik += 1
            
            # Ambil frame saat ini dari parameter
            frame = param
            
            # Ambil warna BGR dan HSV
            bgr_color = frame[y, x]
            hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
            
            # Siapkan rentang saran
            lower_range = [hsv_color[0]-10, 50, 50]
            upper_range = [hsv_color[0]+10, 255, 255]

            # Tampilkan info di console
            print("--------------------")
            print(f"Data ke-{jumlah_klik}/{batas_maksimal}")
            print(f"Koordinat: (x={x}, y={y})")
            print(f"Warna BGR: {bgr_color}")
            print(f"Warna HSV: {hsv_color}")
            print(f"Saran Rentang Bawah (Lower): {lower_range}")
            print(f"Saran Rentang Atas (Upper):   {upper_range}")

            # Buat dictionary untuk data baru
            data_baru = {
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Data Ke': jumlah_klik,
                'X': x, 'Y': y,
                'B': bgr_color[0], 'G': bgr_color[1], 'R': bgr_color[2],
                'H': hsv_color[0], 'S': hsv_color[1], 'V': hsv_color[2],
                'Lower_H': lower_range[0], 'Lower_S': lower_range[1], 'Lower_V': lower_range[2],
                'Upper_H': upper_range[0], 'Upper_S': upper_range[1], 'Upper_V': upper_range[2]
            }
            # Tambahkan data baru ke list penampung
            data_terkumpul.append(data_baru)

        else:
            print("Batas maksimal 200 data telah tercapai.")

# --- Program Utama ---

# Buka webcam
cap = cv2.VideoCapture(2)
if not cap.isOpened():
    print("Error: Tidak dapat membuka kamera.")
    exit()

cv2.namedWindow('Kalibrasi HSV - Klik pada warna')

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Tidak bisa menerima frame.")
        break

    # Cek jika batas maksimal sudah tercapai untuk menghentikan loop
    if jumlah_klik >= batas_maksimal:
        break

    # Set callback mouse
    cv2.setMouseCallback('Kalibrasi HSV - Klik pada warna', mouse_callback, frame)

    # Tampilkan teks status
    info_text = f"Data Terkumpul: {jumlah_klik}/{batas_maksimal}"
    cv2.putText(frame, info_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    if jumlah_klik >= batas_maksimal:
        cv2.putText(frame, "SELESAI!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow('Kalibrasi HSV - Klik pada warna', frame)

    # Keluar jika menekan tombol 'esc'
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

# --- Proses Penyimpanan ke Excel ---
cap.release()
cv2.destroyAllWindows()

# Cek jika ada data yang terkumpul sebelum menyimpan
if data_terkumpul:
    print(f"\nMenyimpan {len(data_terkumpul)} data ke file Excel...")
    
    # Konversi list of dictionary menjadi DataFrame pandas
    df = pd.DataFrame(data_terkumpul)
    
    # Tentukan nama file
    nama_file_excel = 'hasil_kalibrasi_warna.xlsx'
    
    # Simpan DataFrame ke file Excel
    df.to_excel(nama_file_excel, index=False)
    
    print(f"✅ Data berhasil disimpan di: {nama_file_excel}")
else:
    print("\nTidak ada data yang diambil, file Excel tidak dibuat.")