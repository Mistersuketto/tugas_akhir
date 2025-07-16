# PLC/plc_module.py

import time
from fins import FinsClient
import struct # Diperlukan untuk mengubah data byte menjadi integer
>>>>>>> 65d8c24 (hasil terjemahan berhasil diubah ke alamat PLC dan)

# ==============================================================================
# ## BAGIAN 1: FUNGSI UTAMA EKSEKUSI PLC ##
# ==============================================================================

def execute_robot_moves(robot_script, plc_host="192.168.1.28"):
    """
    Menerima skrip perintah robot, terhubung ke PLC, dan mengeksekusi setiap gerakan.
    @param robot_script: String berisi perintah yang dipisahkan spasi (misal: "a+90 U b-90 F2").
    @param plc_host: Alamat IP dari PLC Omron.
    @return: True jika semua perintah berhasil dikirim, False jika terjadi error.
    """
    # --- Peta Alamat PLC ---
    # Mendefinisikan alamat mana yang akan di-trigger untuk setiap perintah
    ROBOT_MOVE_TO_PLC_ADDRESS = {
        "U": "CIO10.0",   "U2": "CIO10.1",   "U'": "CIO10.2",
        "F": "CIO10.3",   "F2": "CIO10.4",   "F'": "CIO10.5",
        "D": "CIO11.0",   "D2": "CIO11.1",   "D'": "CIO11.2",
        "B": "CIO11.3",   "B2": "CIO11.4",   "B'": "CIO11.5",
        "R": "CIO12.0",   "R2": "CIO12.1",   "R'": "CIO12.2",
        "L": "CIO12.3",   "L2": "CIO12.4",   "L'": "CIO12.5",
        "a+90": "CIO13.0", "a-90": "CIO13.1",
        "b+90": "CIO13.2", "b-90": "CIO13.3", "b+180": "CIO13.4", 
        "c+90": "CIO13.5", "c-90": "CIO13.6", "c+180": "CIO13.7",
    }
    
    FEEDBACK_ADDRESS = "D0"
    
    # Pisahkan string perintah menjadi daftar individual
    moves_to_execute = robot_script.strip().split(' ')
    
    client = None
    try:
        print(f"[PLC] Mencoba terhubung ke PLC di {plc_host}...")
        client = FinsClient(host=plc_host)
        client.connect()
        print(f"[PLC] ✅ Berhasil terhubung.")

        # Pastikan D0 dalam keadaan 0 sebelum memulai
        print(f"[PLC] Memastikan feedback di {FEEDBACK_ADDRESS} dalam keadaan awal (0)...")
        client.memory_area_write(FEEDBACK_ADDRESS, b"\x00\x00") # Menulis nilai 0 ke D0

        print(f"\n[PLC] Menerima {len(moves_to_execute)} perintah untuk dieksekusi: {moves_to_execute}")
        print("-" * 40)

        for i, move in enumerate(moves_to_execute):
            print(f"--- Eksekusi Langkah {i+1}/{len(moves_to_execute)}: '{move}' ---")
            
            command_address = ROBOT_MOVE_TO_PLC_ADDRESS.get(move)
            if not command_address:
                print(f"⚠️  Peringatan: Gerakan '{move}' tidak memiliki alamat PLC. Melewati...")
                continue
>>>>>>> 65d8c24 (hasil terjemahan berhasil diubah ke alamat PLC dan)
            
            # Nyalakan bit perintah
            print(f"  -> Mengirim perintah dengan menyalakan bit {command_address}")
            client.memory_area_write(command_address, b"\x01")

            # TAHAP A: Tunggu D0 kembali ke 0 (jika sebelumnya 1, pastikan sinyal lama hilang)
            print(f"  -> Menunggu {FEEDBACK_ADDRESS} untuk siap (nilai 0)...")
            while True:
                response = client.memory_area_read(FEEDBACK_ADDRESS, 1)
                current_feedback_value = struct.unpack('>H', response.data)[0]
                if current_feedback_value == 0:
                    break
                time.sleep(0.1)

            # TAHAP B: Tunggu D0 menjadi 1 (konfirmasi dari PLC bahwa gerakan dimulai/selesai)
            print(f"  -> Menunggu konfirmasi dari PLC ({FEEDBACK_ADDRESS} menjadi 1)...")
            while True:
                response = client.memory_area_read(FEEDBACK_ADDRESS, 1)
                current_feedback_value = struct.unpack('>H', response.data)[0]
                if current_feedback_value == 1:
                    print(f"  -> Konfirmasi diterima! (Nilai {FEEDBACK_ADDRESS} adalah 1)")
                    break
                time.sleep(0.1)
            
            # Matikan kembali bit perintah (PLC akan mereset feedback D0 ke 0)
            print(f"  -> Mereset bit perintah ({command_address} ke 0)")
            client.memory_area_write(command_address, b"\x00")
                        
        print("-" * 40)
        print("\n[PLC] ✅ Semua langkah berhasil dieksekusi!")
        return True

    except Exception as e:
        print(f"\n[PLC] ❌ Terjadi kesalahan saat komunikasi dengan PLC: {e}")
        return False
    finally:
        if client:
            client.close()
            print("[PLC] 🔌 Koneksi ke PLC ditutup.")


# ==============================================================================
# ## BAGIAN 2: BLOK EKSEKUSI (Untuk Testing Mandiri) ##
# ==============================================================================

if __name__ == "__main__":
    print(">>> Menjalankan modul PLC secara mandiri untuk pengujian...")
    
    # Contoh skrip perintah yang akan dihasilkan oleh modul algorithm
    test_script = "a-90 U' b+90 F R2 c-90 L"
    
    # Panggil fungsi utama untuk eksekusi
    execute_robot_moves(test_script)