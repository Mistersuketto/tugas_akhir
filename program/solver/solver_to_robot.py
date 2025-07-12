import sys
import os

# Menambahkan path ke pustaka solver agar bisa di-import
project_path = os.path.abspath('RubiksCube-TwophaseSolver')
if project_path not in sys.path:
    sys.path.append(project_path)

# 1. Impor fungsi 'solve' dari pustaka
from solver import solve

# ===== NOTASI TAMBAHAN =====
set_H1 = {
    "UF": ["U", "F"],   "UR": ["U", "R"],   "UB": ["U", "B"],   "UL": ["U", "L"],   "DF": ["D", "F"],   "DR": ["D", "R"],
    "DB": ["D", "B"],   "DL": ["D", "L"],   "FU": ["F", "U"],   "FR": ["F", "R"],   "FD": ["F", "D"],   "FL": ["F", "L"],
    "BU": ["B", "U"],   "BR": ["B", "R"],   "BD": ["B", "D"],   "BL": ["B", "L"],   "RU": ["R", "U"],   "RF": ["R", "F"],
    "RD": ["R", "D"],   "RB": ["R", "B"],   "LU": ["L", "U"],   "LF": ["L", "F"],   "LD": ["L", "D"],   "LB": ["L", "B"],
}

set_I1 = {
    # kondisi "UF"
    ("UF", "R"): "UR",  ("UF", "L"): "UL",  ("UF", "B"): "UB",  ("UF", "D"): "FD",
    # kondisi "UR"
    ("UR", "B"): "UB",  ("UR", "F"): "UF",  ("UR", "L"): "UL",  ("UR", "D"): "RD",
    # kondisi "UB"
    ("UB", "L"): "UL",  ("UB", "R"): "UR",  ("UB", "F"): "UF",  ("UB", "D"): "BD",
    # kondisi "UL"
    ("UL", "F"): "UF",  ("UL", "B"): "UB",  ("UL", "R"): "UR",  ("UL", "D"): "LD",
    # kondisi "DF"
    ("DF", "L"): "DL",  ("DF", "R"): "DR",  ("DF", "B"): "DB",  ("DF", "U"): "FU",
    # kondisi "DR"
    ("DR", "F"): "DF",  ("DR", "B"): "DB",  ("DR", "L"): "DL",  ("DR", "U"): "RU",
    
    # kondisi "DB"
    ("DB", "R"): "DR",  ("DB", "L"): "DL",  ("DB", "F"): "DF",  ("DB", "U"): "BU",
    # kondisi "DL"
    ("DL", "B"): "DB",  ("DL", "F"): "DF",  ("DL", "R"): "DR",  ("DL", "U"): "LU",
    # kondisi "FU"
    ("FU", "L"): "FL",  ("FU", "R"): "FR",  ("FU", "D"): "FD",  ("FU", "B"): "UB",
    # kondisi "FR"
    ("FR", "U"): "FU",  ("FR", "D"): "FD",  ("FR", "L"): "FL",  ("FR", "B"): "RB",
    # kondisi "FD"
    ("FD", "R"): "FR",  ("FD", "L"): "FL",  ("FD", "U"): "FU",  ("FD", "B"): "DB",
    # kondisi "FL"
    ("FL", "D"): "FD",  ("FL", "U"): "FU",  ("FL", "R"): "FR",  ("FL", "B"): "LB",
    
    # kondisi "BU"
    ("BU", "R"): "BR",  ("BU", "L"): "BL",  ("BU", "D"): "BD",  ("BU", "F"): "UF",
    # kondisi "BR"
    ("BR", "D"): "BD",  ("BR", "U"): "BU",  ("BR", "L"): "BL",  ("BR", "F"): "RF",
    # kondisi "BD"
    ("BD", "L"): "BL",  ("BD", "R"): "BR",  ("BD", "U"): "BU",  ("BD", "F"): "DF",
    # kondisi "BL"
    ("BL", "U"): "BU",  ("BL", "D"): "BD",  ("BL", "R"): "BR",  ("BL", "F"): "LF",
    # kondisi "RU"
    ("RU", "F"): "RF",  ("RU", "B"): "RB",  ("RU", "D"): "RD",  ("RU", "L"): "UL",
    # kondisi "RF"
    ("RF", "D"): "RD",  ("RF", "U"): "RU",  ("RF", "B"): "RB",  ("RF", "L"): "FL",
    
    # kondisi "RD"
    ("RD", "B"): "RB",  ("RD", "F"): "RF",  ("RD", "U"): "RU",  ("RD", "L"): "DL",
    # kondisi "RB"
    ("RB", "U"): "RU",  ("RB", "D"): "RD",  ("RB", "F"): "RF",  ("RB", "L"): "BL",
    # kondisi "LU"
    ("LU", "B"): "LB",  ("LU", "F"): "LF",  ("LU", "D"): "LD",  ("LU", "R"): "UR",
    # kondisi "LF"
    ("LF", "U"): "LU",  ("LF", "D"): "LD",  ("LF", "B"): "LB",  ("LF", "R"): "FR",
    # kondisi "LD"
    ("LD", "F"): "LF",  ("LD", "B"): "LB",  ("LD", "U"): "LU",  ("LD", "R"): "DR",
    # kondisi "LB"
    ("LB", "D"): "LD",  ("LB", "U"): "LU",  ("LB", "F"): "LF",  ("LB", "R"): "BR",
}
# ===== NOTASI TAMBAHAN =====

def create_robot_script(solution_string, initial_orientation="UF"):
    """Menerjemahkan solusi Kociemba menjadi skrip perintah robot."""
    current_orientation = initial_orientation
    total_robotic_cost = 0
    robot_commands = []

    # Bersihkan string solusi menjadi daftar
    moves_list = solution_string.split('(')[0].strip().split(' ')
    if not moves_list or moves_list == ['']:
        return [], 0
    
    print("\nTahap 2: Menerjemahkan solusi menjadi skrip robot...")
    for move in moves_list:
        base_move = move[0]

        if base_move in set_H1.get(current_orientation, []):
            print(f"  - Gerakan '{move}': OK (Orientasi: {current_orientation}, Biaya: +1)")
            robot_commands.append(move)
            total_robotic_cost += 1
        else:
            new_orientation = set_I1.get((current_orientation, base_move))

            if new_orientation:
                print(f"  - Gerakan '{move}': Perlu Re-orientasi ke {new_orientation} (Biaya: +2)")
                robot_commands.append(f"REORIENT_TO_{new_orientation}")
                robot_commands.append(move)
                total_robotic_cost += 2
                current_orientation = new_orientation
            else:
                print(f"Peringatan: Transisi dari {current_orientation} untuk {base_move} tidak ada!")
                robot_commands.append(f"ERROR_UNKNOWN_TRANSITION_FOR_{move}")
    
    return robot_commands, total_robotic_cost

# 2. Definisikan string kubus yang akan dipecahkan
scrambled_cube_string = "BBURUDBFUFFFRRFUUFLULUFUDLRRDBBDBDBLUDDFLLRRBRLLLBRDDF"

# 3. Panggil fungsi solve untuk mendapatkan solusi mentah
print("Tahap 1: Mencari solusi langkah cepat...")
# Kita tidak perlu timeout yang lama karena ini sangat cepat
raw_solution = solve(scrambled_cube_string, max_length=22, timeout=5)

# 4. Tampilkan dan simpan hasilnya
final_script, final_cost = create_robot_script(raw_solution)

# --- TAMPILKAN HASIL AKHIR ---
print("\n" + "="*40)
print("      SKRIP AKHIR UNTUK ROBOT")
print("="*40)
print("Perintah:")
for command in final_script:
    print(f"  -> {command}")
print(f"\nTotal Perkiraan Biaya Robotik: {final_cost}")
print("="*40)