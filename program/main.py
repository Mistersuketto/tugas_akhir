import sys

# --- 1. Impor Semua Modul Fungsional ---
from detection.detection import jalankan_proses_deteksi
from algorithm.algorithm import dapatkan_solusi_robot
from PLC.robot import jalankan_penerjemah_dan_plc

def run_main_process():
    """
    Fungsi utama yang menjalankan seluruh alur kerja dari awal hingga akhir,
    dengan output tambahan untuk maintenance di setiap tahapan.
    """
    print("="*50)
    print("🤖 MEMULAI PROGRAM PENYELESAIAN RUBIK OTOMATIS 🤖")
    print("="*50 + "\n")

    # --- LANGKAH 1: DETEKSI ---
    print("--- [TAHAP 1/3] Mendeteksi Kondisi Rubik dari Kamera ---")
    current_cube_state = jalankan_proses_deteksi()

    # Periksa dan cetak output dari Tahap 1
    print("\n" + "-"*20 + " [MAINTENANCE LOG] " + "-"*20)
    if not current_cube_state:
        print("-> Output Tahap 1 (Deteksi): GAGAL atau Dibatalkan.")
        print("-> Program Berhenti.\n")
        return
    else:
        print(f"-> Output Tahap 1 (Deteksi): String kondisi kubus")
        print(f"   '{current_cube_state}'")
    print("-" * 59 + "\n")

    # --- LANGKAH 2: SOLVER & OPTIMASI ROBOTIK ---
    print("--- [TAHAP 2/3] Mencari Solusi Optimal untuk Robot ---")
    optimal_script = dapatkan_solusi_robot(current_cube_state)

    # Periksa dan cetak output dari Tahap 2
    print("\n" + "-"*20 + " [MAINTENANCE LOG] " + "-"*20)
    if not optimal_script:
        print("-> Output Tahap 2 (Solver): GAGAL menemukan solusi.")
        print("-> Program Berhenti.\n")
        return
    else:
        print(f"-> Output Tahap 2 (Solver): Skrip optimal untuk robot")
        print(f"   '{optimal_script}'")
    print("-" * 59 + "\n")


    # --- LANGKAH 3: PENERJEMAHAN & EKSEKUSI PLC ---
    print("--- [TAHAP 3/3] Menerjemahkan & Mengeksekusi Gerakan via PLC ---")
    
    # Menambahkan jeda untuk konfirmasi sebelum eksekusi fisik
    print("\n*** PERHATIAN: Robot akan segera bergerak! Pastikan area aman. ***")
    try:
        input("Tekan SPASI lalu ENTER untuk memulai penyelesaian fisik...")
    except KeyboardInterrupt:
        print("\nProses dibatalkan oleh pengguna sebelum eksekusi PLC.")
        return

    # Panggil fungsi utama dari modul PLC
    success = jalankan_penerjemah_dan_plc(optimal_script)

    # Periksa dan cetak output dari Tahap 3
    print("\n" + "-"*20 + " [MAINTENANCE LOG] " + "-"*20)
    if success:
        print("-> Output Tahap 3 (PLC): Eksekusi BERHASIL.")
    else:
        print("-> Output Tahap 3 (PLC): Eksekusi GAGAL.")
    print("-" * 59 + "\n")

    # --- PENUTUP ---
    if success:
        print("="*50)
        print("🎉 SELAMAT! SEMUA PROSES SELESAI. RUBIK TELAH DISELESAIKAN! 🎉")
        print("="*50)
    else:
        print("="*50)
        print("❌ PENYELESAIAN GAGAL PADA TAHAP EKSEKUSI PLC ❌")
        print("="*50)


if __name__ == "__main__":
    run_main_process()