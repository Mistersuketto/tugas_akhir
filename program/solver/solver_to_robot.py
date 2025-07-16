import sys
import os

# ==============================================================================
# ## BAGIAN 1: KONFIGURASI DAN PENGETAHUAN ROBOT ##
# ==============================================================================

# --- Pengaturan Path untuk Pustaka Solver ---
# Pastikan nama folder ini sesuai dengan yang ada di lokal Anda
SOLVER_FOLDER_NAME = 'RubiksCube-TwophaseSolver'
project_path = os.path.abspath(SOLVER_FOLDER_NAME)
if project_path not in sys.path:
    sys.path.append(project_path)

try:
    # Impor fungsi 'solve' dari pustaka Kociemba standar
    from solver import solve
except ImportError:
    print(f"Error: Tidak dapat menemukan pustaka di folder '{SOLVER_FOLDER_NAME}'.")
    print("Pastikan nama folder sudah benar dan berada di direktori yang sama dengan skrip ini.")
    sys.exit(1)

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
    # ==========
    # kondisi "UF"
    ("UF", "R"): "RF",  ("UF", "L"): "LF",  ("UF", "B"): "BU",  ("UF", "D"): "DF",
    # kondisi "UR"
    ("UR", "B"): "BR",  ("UR", "F"): "FR",  ("UR", "L"): "LU",  ("UR", "D"): "DR",
    # kondisi "UB"
    ("UB", "L"): "LB",  ("UB", "R"): "RB",  ("UB", "F"): "FU",  ("UB", "D"): "DB",
    # kondisi "UL"
    ("UL", "F"): "FL",  ("UL", "B"): "BL",  ("UL", "R"): "RU",  ("UL", "D"): "DL",
    # kondisi "DF"
    ("DF", "L"): "LF",  ("DF", "R"): "RF",  ("DF", "B"): "BD",  ("DF", "U"): "UF",
    # kondisi "DR"
    ("DR", "F"): "FR",  ("DR", "B"): "BR",  ("DR", "L"): "LD",  ("DR", "U"): "UR",
    
    # kondisi "DB"
    ("DB", "R"): "RB",  ("DB", "L"): "LB",  ("DB", "F"): "FD",  ("DB", "U"): "UB",
    # kondisi "DL"
    ("DL", "B"): "BL",  ("DL", "F"): "FL",  ("DL", "R"): "RD",  ("DL", "U"): "UL",
    # kondisi "FU"
    ("FU", "L"): "LU",  ("FU", "R"): "RU",  ("FU", "D"): "DF",  ("FU", "B"): "BU",
    # kondisi "FR"
    ("FR", "U"): "UR",  ("FR", "D"): "DR",  ("FR", "L"): "LF",  ("FR", "B"): "BR",
    # kondisi "FD"
    ("FD", "R"): "RD",  ("FD", "L"): "LD",  ("FD", "U"): "UF",  ("FD", "B"): "BD",
    # kondisi "FL"
    ("FL", "D"): "DL",  ("FL", "U"): "UL",  ("FL", "R"): "RF",  ("FL", "B"): "BL",

    # kondisi "BU"
    ("BU", "R"): "RU",  ("BU", "L"): "LU",  ("BU", "D"): "DB",  ("BU", "F"): "FU",
    # kondisi "BR"
    ("BR", "D"): "DR",  ("BR", "U"): "UR",  ("BR", "L"): "LB",  ("BR", "F"): "FR",
    # kondisi "BD"
    ("BD", "L"): "LD",  ("BD", "R"): "RD",  ("BD", "U"): "UB",  ("BD", "F"): "FD",
    # kondisi "BL"
    ("BL", "U"): "UL",  ("BL", "D"): "DL",  ("BL", "R"): "RB",  ("BL", "F"): "FL",
    # kondisi "RU"
    ("RU", "F"): "FU",  ("RU", "B"): "BU",  ("RU", "D"): "DR",  ("RU", "L"): "LU",
    # kondisi "RF"
    ("RF", "D"): "DF",  ("RF", "U"): "UF",  ("RF", "B"): "BR",  ("RF", "L"): "LF",
    
    # kondisi "RD"
    ("RD", "B"): "BD",  ("RD", "F"): "FD",  ("RD", "U"): "UR",  ("RD", "L"): "LD",
    # kondisi "RB"
    ("RB", "U"): "UB",  ("RB", "D"): "DB",  ("RB", "F"): "FR",  ("RB", "L"): "LB",
    # kondisi "LU"
    ("LU", "B"): "BU",  ("LU", "F"): "FU",  ("LU", "D"): "DL",  ("LU", "R"): "RU",
    # kondisi "LF"
    ("LF", "U"): "UF",  ("LF", "D"): "DF",  ("LF", "B"): "LB",  ("LF", "R"): "RF",
    # kondisi "LD"
    ("LD", "F"): "FD",  ("LD", "B"): "BD",  ("LD", "U"): "UL",  ("LD", "R"): "RD",
    # kondisi "LB"
    ("LB", "D"): "DB",  ("LB", "U"): "UB",  ("LB", "F"): "FL",  ("LB", "R"): "RB",
}

re_orient = {
    # Rotasi 'a' (Sumbu X)
    ("UF", "FD"): "a+90",   ("UF", "BU"): "a-90", # kondisi "UF"
    ("UR", "RD"): "a+90",   ("UR", "LU"): "a-90", # kondisi "UR"
    ("UB", "BD"): "a+90",   ("UB", "FU"): "a-90", # kondisi "UB"
    ("UL", "LD"): "a+90",   ("UL", "RU"): "a-90", # kondisi "UL"
    ("DF", "FU"): "a+90",   ("DF", "BD"): "a+90", # kondisi "DF"
    ("DR", "RU"): "a+90",   ("DR", "LD"): "a-90", # kondisi "DR"

    ("DB", "BU"): "a+90",   ("DB", "FD"): "a-90", # kondisi "DB"
    ("DL", "LU"): "a+90",   ("DL", "RD"): "a-90", # kondisi "DL"
    ("FU", "UB"): "a+90",   ("FU", "DF"): "a-90", # kondisi "FU"
    ("FR", "RB"): "a+90",   ("FR", "LF"): "a-90", # kondisi "FR"
    ("FD", "DB"): "a+90",   ("FD", "UF"): "a-90", # kondisi "FD"
    ("FL", "LB"): "a+90",   ("FL", "RF"): "a-90", # kondisi "FL"

    ("BU", "UF"): "a+90",   ("BU", "DB"): "a-90", # kondisi "BU"
    ("BR", "RF"): "a+90",   ("BR", "LB"): "a-90", # kondisi "BR"
    ("BD", "DF"): "a+90",   ("BD", "UB"): "a-90", # kondisi "BD"
    ("BL", "LF"): "a+90",   ("BL", "RB"): "a-90", # kondisi "BL"
    ("RU", "UL"): "a+90",   ("RU", "DR"): "a-90", # kondisi "RU"
    ("RF", "FL"): "a+90",   ("RF", "BR"): "a-90", # kondisi "RF"

    ("RD", "DL"): "a+90",   ("RD", "UR"): "a-90", # kondisi "RD"
    ("RB", "BL"): "a+90",   ("RB", "FR"): "a-90", # kondisi "RB"
    ("LU", "UR"): "a+90",   ("LU", "DL"): "a-90", # kondisi "LU"
    ("LF", "FR"): "a+90",   ("LF", "LB"): "a-90", # kondisi "LF"
    ("LD", "DR"): "a+90",   ("LD", "UL"): "a-90", # kondisi "LD"
    ("LB", "BR"): "a+90",   ("LB", "FL"): "a-90", # kondisi "LB"


    # Rotasi 'b' (Sumbu Y)
    ("UF", "UR"): "b+90",   ("UF", "UL"): "b-90",   ("UF", "UB"): "b+180", # kondisi "UF"
    ("UR", "UB"): "b+90",   ("UR", "UF"): "b-90",   ("UR", "UL"): "b+180", # kondisi "UR"
    ("UB", "UL"): "b+90",   ("UB", "UR"): "b-90",   ("UB", "UF"): "b+180", # kondisi "UB"
    ("UL", "UF"): "b+90",   ("UL", "UB"): "b-90",   ("UL", "UR"): "b+180", # kondisi "UL"
    ("DF", "DL"): "b+90",   ("DF", "DR"): "b-90",   ("DF", "DB"): "b+180", # kondisi "DF"
    ("DR", "DF"): "b+90",   ("DR", "DB"): "b-90",   ("DR", "DL"): "b+180", # kondisi "DR"

    ("DB", "DR"): "b+90",   ("DB", "DL"): "b-90",   ("DB", "DF"): "b+180", # kondisi "DB"
    ("DL", "DB"): "b+90",   ("DL", "DF"): "b-90",   ("DL", "DR"): "b+180", # kondisi "DL"
    ("FU", "FL"): "b+90",   ("FU", "FR"): "b-90",   ("FU", "FD"): "b+180", # kondisi "FU"
    ("FR", "FU"): "b+90",   ("FR", "FD"): "b-90",   ("FR", "FL"): "b+180", # kondisi "FR"
    ("FD", "FR"): "b+90",   ("FD", "FL"): "b-90",   ("FD", "FU"): "b+180", # kondisi "FD"
    ("FL", "FD"): "b+90",   ("FL", "FU"): "b-90",   ("FL", "FR"): "b+180", # kondisi "FL"

    ("BU", "BR"): "b+90",   ("BU", "BL"): "b-90",   ("BU", "BD"): "b+180", # kondisi "BU"
    ("BR", "BD"): "b+90",   ("BR", "BU"): "b-90",   ("BR", "BL"): "b+180", # kondisi "BR"
    ("BD", "BL"): "b+90",   ("BD", "BR"): "b-90",   ("BD", "BU"): "b+180", # kondisi "BD"
    ("BL", "BU"): "b+90",   ("BL", "BD"): "b-90",   ("BL", "BR"): "b+180", # kondisi "BL"
    ("RU", "RF"): "b+90",   ("RU", "RB"): "b-90",   ("RU", "RD"): "b+180", # kondisi "RU"
    ("RF", "RD"): "b+90",   ("RF", "RU"): "b-90",   ("RF", "RB"): "b+180", # kondisi "RF"

    ("RD", "RB"): "b+90",   ("RD", "RF"): "b-90",   ("RD", "RU"): "b+180", # kondisi "RD"
    ("RB", "RU"): "b+90",   ("RB", "RD"): "b-90",   ("RB", "RF"): "b+180", # kondisi "RB"
    ("LU", "LB"): "b+90",   ("LU", "LF"): "b-90",   ("LU", "LD"): "b+180", # kondisi "LU"
    ("LF", "LU"): "b+90",   ("LF", "LD"): "b-90",   ("LF", "LB"): "b+180", # kondisi "LF"
    ("LD", "LF"): "b+90",   ("LD", "LB"): "b-90",   ("LD", "LU"): "b+180", # kondisi "LD"
    ("LB", "LD"): "b+90",   ("LB", "LU"): "b-90",   ("LB", "LF"): "b+180", # kondisi "LB"


    # Rotasi 'c' (Sumbu Z)
    ("UF", "RF"): "c+90",   ("UF", "LF"): "c-90",   ("UF", "DF"): "c+180", # kondisi "UF"
    ("UR", "BR"): "c+90",   ("UR", "FR"): "c-90",   ("UR", "DR"): "c+180", # kondisi "UR"
    ("UB", "LB"): "c+90",   ("UB", "RB"): "c-90",   ("UB", "DB"): "c+180", # kondisi "UB"
    ("UL", "FL"): "c+90",   ("UL", "BL"): "c-90",   ("UL", "DL"): "c+180", # kondisi "UL"
    ("DF", "LF"): "c+90",   ("DF", "RF"): "c-90",   ("DF", "UF"): "c+180", # kondisi "DF"
    ("DR", "FR"): "c+90",   ("DR", "BR"): "c-90",   ("DR", "UR"): "c+180", # kondisi "DR"

    ("DB", "RB"): "c+90",   ("DB", "LB"): "c-90",   ("DB", "UB"): "c+180", # kondisi "DB"
    ("DL", "BL"): "c+90",   ("DL", "FL"): "c-90",   ("DL", "UL"): "c+180", # kondisi "DL"
    ("FU", "LU"): "c+90",   ("FU", "RU"): "c-90",   ("FU", "BU"): "c+180", # kondisi "FU"
    ("FR", "UR"): "c+90",   ("FR", "DR"): "c-90",   ("FR", "BR"): "c+180", # kondisi "FR"
    ("FD", "RD"): "c+90",   ("FD", "LD"): "c-90",   ("FD", "BD"): "c+180", # kondisi "FD"
    ("FL", "DL"): "c+90",   ("FL", "UL"): "c-90",   ("FL", "BL"): "c+180", # kondisi "FL"

    ("BU", "RU"): "c+90",   ("BU", "LU"): "c-90",   ("BU", "FU"): "c+180", # kondisi "BU"
    ("BR", "DR"): "c+90",   ("BR", "UR"): "c-90",   ("BR", "FR"): "c+180", # kondisi "BR"
    ("BD", "LD"): "c+90",   ("BD", "RD"): "c-90",   ("BD", "FD"): "c+180", # kondisi "BD"
    ("BL", "UL"): "c+90",   ("BL", "DL"): "c-90",   ("BL", "FL"): "c+180", # kondisi "BL"
    ("RU", "FU"): "c+90",   ("RU", "BU"): "c-90",   ("RU", "LU"): "c+180", # kondisi "RU"
    ("RF", "DF"): "c+90",   ("RF", "UF"): "c-90",   ("RF", "LF"): "c+180", # kondisi "RF"

    ("RD", "BD"): "c+90",   ("RD", "FD"): "c-90",   ("RD", "LD"): "c+180", # kondisi "RD"
    ("RB", "UB"): "c+90",   ("RB", "DB"): "c-90",   ("RB", "LB"): "c+180", # kondisi "RB"
    ("LU", "BU"): "c+90",   ("LU", "FU"): "c-90",   ("LU", "RU"): "c+180", # kondisi "LU"
    ("LF", "UF"): "c+90",   ("LF", "DF"): "c-90",   ("LF", "RF"): "c+180", # kondisi "LF"
    ("LD", "FD"): "c+90",   ("LD", "BD"): "c-90",   ("LD", "RD"): "c+180", # kondisi "LD"
    ("LB", "DB"): "c+90",   ("LB", "UB"): "c-90",   ("LB", "RB"): "c+180", # kondisi "LB"
}
# ===== NOTASI TAMBAHAN =====

# ==============================================================================
# ## BAGIAN 2: ALGORITMA PENERJEMAH TAHAP KEDUA ##
# ==============================================================================

def create_robot_script(solution_string, initial_orientation="UF"):
    """
    Menerjemahkan solusi Kociemba standar menjadi skrip perintah robot
    yang terdiri dari 16 gerakan dasar.
    """
    current_orientation = initial_orientation
    robot_commands = []

    # Bersihkan string solusi menjadi daftar, tangani jika kosong
    moves_list = solution_string.split('(')[0].strip().split(' ')
    if not moves_list or moves_list == ['']:
        return []

    print("\n[Tahap 2] Menerjemahkan solusi menjadi skrip robot...")
    for move in moves_list:
        base_move = move[0] # Dapatkan gerakan dasar (misal, dari "R'", "R2", dasarnya adalah "R")

        # Periksa apakah gerakan bisa dilakukan langsung
        if base_move in set_H1.get(current_orientation, []):
            print(f"  - Gerakan '{move}': OK (Orientasi: {current_orientation})")
            robot_commands.append(move)
        else:
            # Jika tidak, cari orientasi baru yang diperlukan
            new_orientation = set_I1.get((current_orientation, base_move))
            
            if new_orientation:
                # Cari perintah re-orientasi yang spesifik dari kamus mapping
                reorient_command = RE_ORIENT_MAP.get((current_orientation, new_orientation))
                
                if reorient_command:
                    print(f"  - Gerakan '{move}': Perlu Re-orientasi dari {current_orientation} ke {new_orientation}")
                    print(f"    -> Perintah Re-orientasi: {reorient_command}")
                    
                    robot_commands.append(reorient_command)
                    robot_commands.append(move) # Tambahkan gerakan putar setelahnya
                    current_orientation = new_orientation # Perbarui orientasi robot
                else:
                    # Menangani jika transisi ada di set_I1 tapi tidak ada di RE_ORIENT_MAP
                    error_msg = f"ERROR_CMD_UNDEFINED_FOR_{current_orientation}_TO_{new_orientation}"
                    print(f"Peringatan: Perintah untuk transisi dari {current_orientation} ke {new_orientation} tidak terdefinisi!")
                    robot_commands.append(error_msg)
            else:
                # Menangani jika transisi tidak ada di set_I1
                error_msg = f"ERROR_UNKNOWN_TRANSITION_FOR_{move}_FROM_{current_orientation}"
                print(f"Peringatan: Transisi dari {current_orientation} untuk {base_move} tidak ada!")
                robot_commands.append(error_msg)
    
    return robot_commands

# ==============================================================================
# ## BAGIAN 3: ALUR UTAMA PROGRAM ##
# ==============================================================================

if __name__ == "__main__":
    # Definisikan string kubus
    scrambled_cube_string = "DUUBULDBFRBFRRULLLBRDFFFBLURDBFDFDRFRULBLUFDURRBLBDUDL"

    # --- TAHAP 1: DAPATKAN SOLUSI CEPAT ---
    print("[Tahap 1] Mencari solusi langkah standar...")
    # Menggunakan pustaka Kociemba standar yang cepat
    raw_solution = solve(scrambled_cube_string, max_length=22, timeout=10)
    print(f"Solusi mentah ditemukan: {raw_solution}")

    # --- TAHAP 2: JALANKAN PENERJEMAH ---
    # Memanggil fungsi penerjemah dengan solusi mentah sebagai input
    final_script = create_robot_script(raw_solution)

    # --- TAMPILKAN HASIL AKHIR ---
    print("\n" + "="*40)
    print("      SKRIP AKHIR UNTUK ROBOT")
    print("="*40)
    print("Perintah:")
    # Cetak setiap perintah dalam format yang rapi
    for command in final_script:
        print(f"  -> {command}")
    print("="*40)