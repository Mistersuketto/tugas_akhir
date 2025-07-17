# --- 1. Impor Semua Modul Fungsional ---
from detection.detection import jalankan_proses_deteksi
from algorithm.algorithm import dapatkan_solusi_robot
from PLC.robot import jalankan_penerjemah_dan_plc # <-- Ganti nama fungsi ini

def run_main_process():
    """
    Fungsi utama yang menjalankan seluruh alur kerja dari awal hingga akhir.
    """
    print("="*50)
    print("🤖 MEMULAI PROGRAM PENYELESAIAN RUBIK OTOMATIS 🤖")
    print("="*50 + "\n")

    # --- LANGKAH 1: DETEKSI ---
    print("--- [TAHAP 1/3] Mendeteksi Kondisi Rubik dari Kamera ---")
    current_cube_state = jalankan_proses_deteksi()
    if not current_cube_state:
        print("\n❌ Proses deteksi gagal atau dibatalkan. Program berhenti."); return

    print("\n[✔] Deteksi berhasil.\n")

    # --- LANGKAH 2: SOLVER & OPTIMASI ROBOTIK ---
    print("--- [TAHAP 2/3] Mencari Solusi Optimal untuk Robot ---")
    optimal_script = dapatkan_solusi_robot(current_cube_state)
    if not optimal_script:
        print("\n❌ Proses solving gagal menemukan solusi. Program berhenti."); return
        
    print(f"\n[✔] Solusi optimal berhasil dibuat: {optimal_script}\n")

    # --- LANGKAH 3: PENERJEMAHAN & EKSEKUSI PLC ---
    print("--- [TAHAP 3/3] Menerjemahkan & Mengeksekusi Gerakan via PLC ---")
    # Panggil fungsi utama dari modul PLC dengan hasil dari tahap 2
    success = jalankan_penerjemah_dan_plc(optimal_script)
    if not success:
        print("\n❌ Proses PLC gagal. Periksa koneksi atau logika PLC."); return

    print("\n" + "="*50)
    print("🎉 SELAMAT! SEMUA PROSES SELESAI. RUBIK TELAH DISELESAIKAN! 🎉")
    print("="*50)

if __name__ == "__main__":
    run_main_process()