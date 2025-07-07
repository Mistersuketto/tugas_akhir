import cv2
import numpy as np

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Ambil frame saat ini dari parameter
        frame = param
        
        # Ambil warna BGR dari pixel yang di-klik
        bgr_color = frame[y, x]
        
        # Konversi BGR ke HSV
        # Kita perlu mengubahnya menjadi array 3D agar fungsi konversi bekerja
        hsv_color = cv2.cvtColor(np.uint8([[bgr_color]]), cv2.COLOR_BGR2HSV)[0][0]
        
        print("--------------------")
        print(f"Koordinat: (x={x}, y={y})")
        print(f"Warna BGR: {bgr_color}")
        print(f"Warna HSV: {hsv_color}")
        print("Saran Rentang Bawah (Lower): [{}, {}, {}]".format(hsv_color[0]-10, hsv_color[1]-40, hsv_color[2]-40))
        print("Saran Rentang Atas (Upper):   [{}, {}, {}]".format(hsv_color[0]+10, 255, 255))


# Buka webcam
cap = cv2.VideoCapture(0)

cv2.namedWindow('Kalibrasi HSV - Klik pada warna')

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    # Set callback mouse, lewatkan frame saat ini sebagai parameter
    cv2.setMouseCallback('Kalibrasi HSV - Klik pada warna', mouse_callback, frame)

    cv2.imshow('Kalibrasi HSV - Klik pada warna', frame)

    # Keluar jika menekan tombol 'esc'
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()