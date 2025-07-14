# control_lamp_from_repo.py

# Impor kelas utama dari library
from fins import FinsClient

# --- KONFIGURASI ---
PLC_IP_ADDRESS = '192.168.1.28'  # Gunakan IP address PLC Anda
PLC_PORT = 9600
# Alamat ditulis sebagai string biasa, sesuai dokumentasi
LAMP_ADDRESS = "CIO10.00"

# Membuat instance dari FinsClient
# Opsi mode='tcp' atau 'udp' bisa ditambahkan, defaultnya adalah 'udp'
client = FinsClient(host=PLC_IP_ADDRESS, port=PLC_PORT, mode='tcp')

try:
    # 1. Membuka koneksi ke PLC
    print(f"Menyambungkan ke PLC di {PLC_IP_ADDRESS}...")
    client.connect()
    print("✅ Koneksi berhasil!")
    print("-" * 30)

    while True:
        command = input("Ketik 'on' untuk menyalakan, 'off' untuk mematikan, atau 'exit' untuk keluar: ").lower()

        if command == 'exit':
            break

        if command == 'on':
            # Data untuk menyalakan bit adalah b'\x01'
            value_to_write = b'\x01'
            action_text = "MENYALAKAN"
        elif command == 'off':
            # Data untuk mematikan bit adalah b'\x00'
            value_to_write = b'\x00'
            action_text = "MEMATIKAN"
        else:
            print("Perintah tidak valid.")
            continue

        try:
            # 2. Mengirim perintah untuk menulis ke alamat memori
            # Fungsi ini akan menangani pembuatan header dan frame FINS secara otomatis
            print(f"Mengirim perintah untuk {action_text} lampu di alamat {LAMP_ADDRESS}...")
            response = client.memory_area_write(LAMP_ADDRESS, value_to_write)

            # 3. Memeriksa status respons dari PLC
            if response.ok:
                print(f"✅ Lampu berhasil di-{action_text}! (Status: {response.status_text})")
            else:
                # Menampilkan pesan error jika PLC menolak perintah
                print(f"⚠️ Gagal! PLC merespons dengan error: {response.status_text}")
            
            print("-" * 30)

        except Exception as e:
            print(f"❌ Terjadi error saat mengirim perintah: {e}")


except Exception as e:
    print(f"❌ Gagal terhubung ke PLC: {e}")

finally:
    # 4. Menutup koneksi setelah selesai
    # Metode .close() tersedia di FinsClient
    print("Menutup koneksi...")
    client.close()