from ultralytics import YOLO
import cv2
import numpy as np

# Muat model YOLOv8 Segmentasi yang sudah Anda latih
# Pastikan model ini dilatih untuk mendeteksi satu kelas saja: "piece" atau "sticker"
try:
    model = YOLO("yolov8m-seg.pt") # Ganti dengan nama file .pt Anda
except Exception as e:
    print(f"Error loading model: {e}")
    print("Pastikan file 'yolov8m-seg.pt' ada di direktori yang sama.")
    exit()


# Buka webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Tidak dapat membuka kamera.")
    exit()

# Definisikan rentang HSV untuk setiap warna Rubik's Cube
# Format untuk MERAH diubah untuk menangani rentang hue yang terpisah (0-10 dan 170-180)
color_ranges = {
    'U (Putih)': (([0, 0, 150], [180, 50, 255])),
    'R (Merah)': (([0, 100, 100], [10, 255, 255]), ([160, 100, 100], [180, 255, 255])),
    'F (Hijau)': (([40, 50, 50], [90, 255, 255])),
    'D (Kuning)':(([20, 100, 100], [40, 255, 255])),
    'L (Oranye)':(([10, 100, 100], [25, 255, 255])),
    'B (Biru)':  (([90, 50, 50], [130, 255, 255]))
}

def get_color_name(hsv_roi):
    """Mendeteksi warna dari ROI (Region of Interest) berdasarkan rentang HSV."""
    max_area = 0
    detected_color = None

    for color_name, hsv_range in color_ranges.items():
        if color_name == 'R (Merah)':
            # Proses rentang ganda untuk warna merah
            lower1, upper1 = np.array(hsv_range[0], dtype=np.uint8)
            lower2, upper2 = np.array(hsv_range[1], dtype=np.uint8)
            mask1 = cv2.inRange(hsv_roi, lower1, upper1)
            mask2 = cv2.inRange(hsv_roi, lower2, upper2)
            mask = cv2.bitwise_or(mask1, mask2)
        else:
            # Proses rentang tunggal untuk warna lain
            lower, upper = np.array(hsv_range[0], dtype=np.uint8)
            mask = cv2.inRange(hsv_roi, lower, upper)
        
        # Hitung jumlah piksel yang cocok
        area = cv2.countNonZero(mask)

        # Simpan warna dengan area terbesar
        if area > max_area:
            max_area = area
            detected_color = color_name
    
    return detected_color


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Buat kanvas kosong untuk menampilkan semua mask segmentasi
    combined_mask_display = np.zeros(frame.shape[:2], dtype=np.uint8)
    
    # Lakukan prediksi dengan model YOLO
    results = model.predict(source=frame, conf=0.4, verbose=False)

    if results and results[0].masks is not None:
        # Ambil semua mask dan box dari hasil prediksi
        masks = results[0].masks.cpu().numpy()
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)

        for i, mask_data in enumerate(masks):
            # Buat mask biner dari poligon segmentasi
            mask = cv2.resize(mask_data, (frame.shape[1], frame.shape[0])).astype(np.uint8)
            
            # Tambahkan mask ini ke kanvas gabungan untuk ditampilkan
            combined_mask_display = cv2.bitwise_or(combined_mask_display, mask * 255)

            # Ekstrak ROI menggunakan mask (jauh lebih akurat daripada bounding box)
            roi_masked = cv2.bitwise_and(frame, frame, mask=mask)
            
            # Konversi ROI yang sudah di-mask ke HSV
            hsv_roi = cv2.cvtColor(roi_masked, cv2.COLOR_BGR2HSV)
            
            # Dapatkan nama warna dari ROI
            color_name = get_color_name(hsv_roi)

            if color_name:
                # Ambil koordinat bounding box untuk menempatkan teks
                x1, y1, _, _ = boxes[i]
                cv2.putText(frame, color_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 3)
                cv2.putText(frame, color_name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # Gambar kontur segmentasi pada frame utama
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)


    # Tampilkan hasil
    cv2.imshow("Deteksi Warna Rubik", frame)
    cv2.imshow("Mask Segmentasi Gabungan", combined_mask_display)

    # Tombol ESC untuk keluar
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()