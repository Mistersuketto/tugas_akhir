# main.py

# --- Impor Modul ---
from detection.detection import jalankan_proses_deteksi
from algorithm.algorithm import dapatkan_solusi_robot
# from PLC.plc_module import execute_robot_moves # Untuk langkah selanjutnya

def main():
    """
    Fungsi utama yang menjalankan seluruh alur kerja.
    """
    print("=============================================")
    print("MEMULAI PROGRAM PENYELESAIAN RUBIK OTOMATIS")
    print("=============================================\n")

    # --- LANGKAH 1: DETEKSI ---
    print("--- LANGKAH 1: Mendeteksi Kondisi Rubik ---")
    current_cube_state = jalankan_proses_deteksi()

    if not current_cube_state:
        print("\nProses deteksi gagal atau dibatalkan. Program berhenti.")
        return

    print("\nStatus: Deteksi berhasil. String yang diterima:")
    print(f"-> {current_cube_state}\n")

    # --- LANGKAH 2: SOLVER ---
    print("--- LANGKAH 2: Mencari Solusi Optimal untuk Robot ---")
    # Panggil fungsi dari modul solver dengan output dari langkah 1
    robot_solution_script = dapatkan_solusi_robot(current_cube_state)

    if not robot_solution_script:
        print("\nProses solving gagal menemukan solusi. Program berhenti.")
        return

    print("\nStatus: Solusi robotik berhasil dibuat. Skrip perintah:")
    print(f"-> {robot_solution_script}\n")

    # --- LANGKAH 3: KONTROL PLC (Placeholder untuk sekarang) ---
    print("--- LANGKAH 3: Mengeksekusi Gerakan Robot via PLC ---")
    print(f"Skrip '{robot_solution_script}' akan dikirim ke PLC...")
    # execute_robot_moves(robot_solution_script)
    print("Status: Langkah PLC akan diimplementasikan di sini.\n")

    print("=============================================")
    print("PROSES SELESAI.")
    print("=============================================")


if __name__ == "__main__":
    main()