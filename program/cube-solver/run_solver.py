# 1. Impor class SolutionManager dari file yang telah Anda modifikasi
from twophase import SolutionManager

# 2. Definisikan string kubus yang diacak (scrambled cube)
#    Ini adalah contoh kubus yang valid. Ganti dengan string dari kubus Anda.
scrambled_cube_string = "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB" # Contoh solved
# Contoh lain yang acak:
# scrambled_cube_string = "DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL"

# 3. Buat objek dari class SolutionManager
#    Langkah ini akan memverifikasi string kubus dan melakukan inisialisasi.
try:
    solver = SolutionManager(scrambled_cube_string)

    # 4. Panggil metode solve()
    #    'max_length' sekarang berarti batas MAKSIMUM BIAYA ROBOTIK, bukan jumlah gerakan.
    #    'timeout' adalah batas waktu dalam detik.
    print("Mencari solusi untuk kubus...")
    solution = solver.solve(max_length=60, timeout=360)

    # 5. Tampilkan hasilnya
    if isinstance(solution, str):
        print("\nSolusi Ditemukan:")
        print(solution)
        
        # Anda juga bisa melihat 'biaya' total dari solusi tersebut
        # (meskipun kode untuk menampilkan ini perlu ditambahkan secara eksplisit)
        
    elif solution == -1:
        print("\nTidak ada solusi yang ditemukan dalam batas biaya dan waktu yang ditentukan.")
    elif solution == -2:
        print("\nBatas waktu (timeout) tercapai.")

except ValueError as e:
    print(f"Error: {e}")