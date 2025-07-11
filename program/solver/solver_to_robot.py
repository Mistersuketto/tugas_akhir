import sys
import os

# Menambahkan path ke pustaka solver agar bisa di-import
project_path = os.path.abspath('RubiksCube-TwophaseSolver')
if project_path not in sys.path:
    sys.path.append(project_path)

# 1. Impor fungsi 'solve' dari pustaka
from solver import solve

# 2. Definisikan string kubus yang akan dipecahkan
scrambled_cube_string = "DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL"

# 3. Panggil fungsi solve untuk mendapatkan solusi mentah
print("Tahap 1: Mencari solusi langkah cepat...")
# Kita tidak perlu timeout yang lama karena ini sangat cepat
raw_solution = solve(scrambled_cube_string, max_length=22, timeout=5)

# 4. Tampilkan dan simpan hasilnya
print(f"Solusi mentah ditemukan: {raw_solution}")

# Hasil ini (misal: "R U' F2 ... (20f)") adalah bahan baku
# yang akan kita gunakan di Tahap 2.
# Kita bisa membersihkannya untuk mendapatkan daftar gerakan murni.
if '(' in raw_solution:
    # Mengambil hanya bagian gerakannya saja
    solution_moves = raw_solution.split('(')[0].strip().split(' ')
    print(f"Daftar gerakan murni: {solution_moves}")