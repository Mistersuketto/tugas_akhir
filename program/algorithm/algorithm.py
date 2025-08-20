# solver/solver_module.py

import sys
import os
import time

# ==============================================================================
# ## BAGIAN 1: KONFIGURASI DAN PUSTAKA (Sedikit modifikasi) ##
# ==============================================================================

# Pengaturan Path: Ini penting agar bisa menemukan pustaka Kociemba
# Pastikan folder 'RubiksCube-TwophaseSolver' berada di dalam folder 'solver'
try:
    SOLVER_FOLDER_NAME = 'RubiksCube-TwophaseSolver'
    # Membuat path relatif terhadap file ini
    project_path = os.path.join(os.path.dirname(__file__), SOLVER_FOLDER_NAME)
    if project_path not in sys.path:
        sys.path.append(project_path)
    from solver import solve as kociemba_solve
except ImportError:
    print(f"FATAL ERROR: Tidak dapat menemukan pustaka di '{project_path}'.")
    print("Pastikan folder 'RubiksCube-TwophaseSolver' ada di dalam direktori 'solver'.")
    sys.exit(1)

# --- Definisi Notasi Gerakan Robot Anda (Tidak ada perubahan) ---
# ===== NOTASI TAMBAHAN =====
set_H1 = {
    "UF": ["U", "F"],   "UR": ["U", "R"],   "UB": ["U", "B"],   "UL": ["U", "L"],
    "DF": ["D", "F"],   "DR": ["D", "R"],   "DB": ["D", "B"],   "DL": ["D", "L"],
    "FU": ["F", "U"],   "FR": ["F", "R"],   "FD": ["F", "D"],   "FL": ["F", "L"],
    "BU": ["B", "U"],   "BR": ["B", "R"],   "BD": ["B", "D"],   "BL": ["B", "L"],
    "RU": ["R", "U"],   "RF": ["R", "F"],   "RD": ["R", "D"],   "RB": ["R", "B"],
    "LU": ["L", "U"],   "LF": ["L", "F"],   "LD": ["L", "D"],   "LB": ["L", "B"],
}

set_I1 = {
    # kondisi "UF"
    ("UF", "R"): ["UR", "RF"],  ("UF", "L"): ["UL", "LF"],  ("UF", "B"): ["UB", "BU"],  ("UF", "D"): ["FD", "DF"],
    # kondisi "UR"
    ("UR", "B"): ["UB", "BR"],  ("UR", "F"): ["UF", "FR"],  ("UR", "L"): ["UL", "LU"],  ("UR", "D"): ["RD", "DR"],
    # kondisi "UB"
    ("UB", "L"): ["UL", "LB"],  ("UB", "R"): ["UR", "RB"],  ("UB", "F"): ["UF", "FU"],  ("UB", "D"): ["BD", "DB"],
    # kondisi "UL"
    ("UL", "F"): ["UF", "FL"],  ("UL", "B"): ["UB", "BL"],  ("UL", "R"): ["UR", "RU"],  ("UL", "D"): ["LD", "DL"],
    # ==========U==========

    # kondisi "DF"
    ("DF", "L"): ["DL", "LF"],  ("DF", "R"): ["DR", "RF"],  ("DF", "B"): ["DB", "BD"],  ("DF", "U"): ["FU", "UF"],
    # kondisi "DR"
    ("DR", "F"): ["DF", "FR"],  ("DR", "B"): ["DB", "BR"],  ("DR", "L"): ["DL", "LD"],  ("DR", "U"): ["RU", "UR"],
    # kondisi "DB"
    ("DB", "R"): ["DR", "RB"],  ("DB", "L"): ["DL", "LB"],  ("DB", "F"): ["DF", "FD"],  ("DB", "U"): ["BU", "UB"],
    # kondisi "DL"
    ("DL", "B"): ["DB", "BL"],  ("DL", "F"): ["DF", "FL"],  ("DL", "R"): ["DR", "RD"],  ("DL", "U"): ["LU", "UL"],
    # ==========D==========

    # kondisi "FU"
    ("FU", "L"): ["FL", "LU"],  ("FU", "R"): ["FR", "RU"],  ("FU", "D"): ["FD", "DF"],  ("FU", "B"): ["UB", "BU"],
    # kondisi "FR"
    ("FR", "U"): ["FU", "UR"],  ("FR", "D"): ["FD", "DR"],  ("FR", "L"): ["FL", "LF"],  ("FR", "B"): ["RB", "BR"],
    # kondisi "FD"
    ("FD", "R"): ["FR", "RD"],  ("FD", "L"): ["FL", "LD"],  ("FD", "U"): ["FU", "UF"],  ("FD", "B"): ["DB", "BD"],
    # kondisi "FL"
    ("FL", "D"): ["FD", "DL"],  ("FL", "U"): ["FU", "UL"],  ("FL", "R"): ["FR", "RF"],  ("FL", "B"): ["LB", "BL"],
    # ==========F==========

    # kondisi "BU"
    ("BU", "R"): ["BR", "RU"],  ("BU", "L"): ["BL", "LU"],  ("BU", "D"): ["BD", "DB"],  ("BU", "F"): ["UF", "FU"],
    # kondisi "BR"
    ("BR", "D"): ["BD", "DR"],  ("BR", "U"): ["BU", "UR"],  ("BR", "L"): ["BL", "LB"],  ("BR", "F"): ["RF", "FR"],
    # kondisi "BD"
    ("BD", "L"): ["BL", "LD"],  ("BD", "R"): ["BR", "RD"],  ("BD", "U"): ["BU", "UB"],  ("BD", "F"): ["DF", "FD"],
    # kondisi "BL"
    ("BL", "U"): ["BU", "UL"],  ("BL", "D"): ["BD", "DL"],  ("BL", "R"): ["BR", "RB"],  ("BL", "F"): ["LF", "FL"],
    # ==========B==========

    # kondisi "RU"
    ("RU", "F"): ["RF", "FU"],  ("RU", "B"): ["RB", "BU"],  ("RU", "D"): ["RD", "DR"],  ("RU", "L"): ["UL", "LU"],
    # kondisi "RF"
    ("RF", "D"): ["RD", "DF"],  ("RF", "U"): ["RU", "UF"],  ("RF", "B"): ["RB", "BR"],  ("RF", "L"): ["FL", "LF"],
    # kondisi "RD"
    ("RD", "B"): ["RB", "BD"],  ("RD", "F"): ["RF", "FD"],  ("RD", "U"): ["RU", "UR"],  ("RD", "L"): ["DL", "LD"],
    # kondisi "RB"
    ("RB", "U"): ["RU", "UB"],  ("RB", "D"): ["RD", "DB"],  ("RB", "F"): ["RF", "FR"],  ("RB", "L"): ["BL", "LB"],
    # ==========R==========

    # kondisi "LU"
    ("LU", "B"): ["LB", "BU"],  ("LU", "F"): ["LF", "FU"],  ("LU", "D"): ["LD", "DL"],  ("LU", "R"): ["UR", "RU"],
    # kondisi "LF"
    ("LF", "U"): ["LU", "UF"],  ("LF", "D"): ["LD", "DF"],  ("LF", "B"): ["LB", "LB"],  ("LF", "R"): ["FR", "RF"],
    # kondisi "LD"
    ("LD", "F"): ["LF", "FD"],  ("LD", "B"): ["LB", "BD"],  ("LD", "U"): ["LU", "UL"],  ("LD", "R"): ["DR", "RD"],
    # kondisi "LB"
    ("LB", "D"): ["LD", "DB"],  ("LB", "U"): ["LU", "UB"],  ("LB", "F"): ["LF", "FL"],  ("LB", "R"): ["BR", "RB"],
    # ==========L==========
}

re_orient = {
    # Rotasi 'a' (Sumbu X)
    ("UF", "FD"): ("a+90", 2),    ("UF", "BU"): ("a-90", 2),
    ("UR", "RD"): ("a+90", 2),    ("UR", "LU"): ("a-90", 2),
    ("UB", "BD"): ("a+90", 2),    ("UB", "FU"): ("a-90", 2),
    ("UL", "LD"): ("a+90", 2),    ("UL", "RU"): ("a-90", 2),
    ("DF", "FU"): ("a+90", 2),    ("DF", "BD"): ("a-90", 2),
    ("DR", "RU"): ("a+90", 2),    ("DR", "LD"): ("a-90", 2),
    ("DB", "BU"): ("a+90", 2),    ("DB", "FD"): ("a-90", 2),
    ("DL", "LU"): ("a+90", 2),    ("DL", "RD"): ("a-90", 2),
    ("FU", "UB"): ("a+90", 2),    ("FU", "DF"): ("a-90", 2),
    ("FR", "RB"): ("a+90", 2),    ("FR", "LF"): ("a-90", 2),
    ("FD", "DB"): ("a+90", 2),    ("FD", "UF"): ("a-90", 2),
    ("FL", "LB"): ("a+90", 2),    ("FL", "RF"): ("a-90", 2),
    ("BU", "UF"): ("a+90", 2),    ("BU", "DB"): ("a-90", 2),
    ("BR", "RF"): ("a+90", 2),    ("BR", "LB"): ("a-90", 2),
    ("BD", "DF"): ("a+90", 2),    ("BD", "UB"): ("a-90", 2),
    ("BL", "LF"): ("a+90", 2),    ("BL", "RB"): ("a-90", 2),
    ("RU", "UL"): ("a+90", 2),    ("RU", "DR"): ("a-90", 2),
    ("RF", "FL"): ("a+90", 2),    ("RF", "BR"): ("a-90", 2),
    ("RD", "DL"): ("a+90", 2),    ("RD", "UR"): ("a-90", 2),
    ("RB", "BL"): ("a+90", 2),    ("RB", "FR"): ("a-90", 2),
    ("LU", "UR"): ("a+90", 2),    ("LU", "DL"): ("a-90", 2),
    ("LF", "FR"): ("a+90", 2),    ("LF", "LB"): ("a-90", 2),
    ("LD", "DR"): ("a+90", 2),    ("LD", "UL"): ("a-90", 2),
    ("LB", "BR"): ("a+90", 2),    ("LB", "FL"): ("a-90", 2),

    # Rotasi 'b' (Sumbu Y)
    ("UF", "UR"): ("b+90", 2),    ("UF", "UL"): ("b-90", 2),    ("UF", "UB"): ("b+180", 3),
    ("UR", "UB"): ("b+90", 2),    ("UR", "UF"): ("b-90", 2),    ("UR", "UL"): ("b+180", 3),
    ("UB", "UL"): ("b+90", 2),    ("UB", "UR"): ("b-90", 2),    ("UB", "UF"): ("b+180", 3),
    ("UL", "UF"): ("b+90", 2),    ("UL", "UB"): ("b-90", 2),    ("UL", "UR"): ("b+180", 3),
    ("DF", "DL"): ("b+90", 2),    ("DF", "DR"): ("b-90", 2),    ("DF", "DB"): ("b+180", 3),
    ("DR", "DF"): ("b+90", 2),    ("DR", "DB"): ("b-90", 2),    ("DR", "DL"): ("b+180", 3),
    ("DB", "DR"): ("b+90", 2),    ("DB", "DL"): ("b-90", 2),    ("DB", "DF"): ("b+180", 3),
    ("DL", "DB"): ("b+90", 2),    ("DL", "DF"): ("b-90", 2),    ("DL", "DR"): ("b+180", 3),
    ("FU", "FL"): ("b+90", 2),    ("FU", "FR"): ("b-90", 2),    ("FU", "FD"): ("b+180", 3),
    ("FR", "FU"): ("b+90", 2),    ("FR", "FD"): ("b-90", 2),    ("FR", "FL"): ("b+180", 3),
    ("FD", "FR"): ("b+90", 2),    ("FD", "FL"): ("b-90", 2),    ("FD", "FU"): ("b+180", 3),
    ("FL", "FD"): ("b+90", 2),    ("FL", "FU"): ("b-90", 2),    ("FL", "FR"): ("b+180", 3),
    ("BU", "BR"): ("b+90", 2),    ("BU", "BL"): ("b-90", 2),    ("BU", "BD"): ("b+180", 3),
    ("BR", "BD"): ("b+90", 2),    ("BR", "BU"): ("b-90", 2),    ("BR", "BL"): ("b+180", 3),
    ("BD", "BL"): ("b+90", 2),    ("BD", "BR"): ("b-90", 2),    ("BD", "BU"): ("b+180", 3),
    ("BL", "BU"): ("b+90", 2),    ("BL", "BD"): ("b-90", 2),    ("BL", "BR"): ("b+180", 3),
    ("RU", "RF"): ("b+90", 2),    ("RU", "RB"): ("b-90", 2),    ("RU", "RD"): ("b+180", 3),
    ("RF", "RD"): ("b+90", 2),    ("RF", "RU"): ("b-90", 2),    ("RF", "RB"): ("b+180", 3),
    ("RD", "RB"): ("b+90", 2),    ("RD", "RF"): ("b-90", 2),    ("RD", "RU"): ("b+180", 3),
    ("RB", "RU"): ("b+90", 2),    ("RB", "RD"): ("b-90", 2),    ("RB", "RF"): ("b+180", 3),
    ("LU", "LB"): ("b+90", 2),    ("LU", "LF"): ("b-90", 2),    ("LU", "LD"): ("b+180", 3),
    ("LF", "LU"): ("b+90", 2),    ("LF", "LD"): ("b-90", 2),    ("LF", "LB"): ("b+180", 3),
    ("LD", "LF"): ("b+90", 2),    ("LD", "LB"): ("b-90", 2),    ("LD", "LU"): ("b+180", 3),
    ("LB", "LD"): ("b+90", 2),    ("LB", "LU"): ("b-90", 2),    ("LB", "LF"): ("b+180", 3),

    # Rotasi 'c' (Sumbu Z)
    ("UF", "RF"): ("c-90", 2),    ("UF", "LF"): ("c+90", 2),    ("UF", "DF"): ("c+180", 3),
    ("UR", "BR"): ("c-90", 2),    ("UR", "FR"): ("c+90", 2),    ("UR", "DR"): ("c+180", 3),
    ("UB", "LB"): ("c-90", 2),    ("UB", "RB"): ("c+90", 2),    ("UB", "DB"): ("c+180", 3),
    ("UL", "FL"): ("c-90", 2),    ("UL", "BL"): ("c+90", 2),    ("UL", "DL"): ("c+180", 3),
    ("DF", "LF"): ("c-90", 2),    ("DF", "RF"): ("c+90", 2),    ("DF", "UF"): ("c+180", 3),
    ("DR", "FR"): ("c-90", 2),    ("DR", "BR"): ("c+90", 2),    ("DR", "UR"): ("c+180", 3),
    ("DB", "RB"): ("c-90", 2),    ("DB", "LB"): ("c+90", 2),    ("DB", "UB"): ("c+180", 3),
    ("DL", "BL"): ("c-90", 2),    ("DL", "FL"): ("c+90", 2),    ("DL", "UL"): ("c+180", 3),
    ("FU", "LU"): ("c-90", 2),    ("FU", "RU"): ("c+90", 2),    ("FU", "BU"): ("c+180", 3),
    ("FR", "UR"): ("c-90", 2),    ("FR", "DR"): ("c+90", 2),    ("FR", "BR"): ("c+180", 3),
    ("FD", "RD"): ("c-90", 2),    ("FD", "LD"): ("c+90", 2),    ("FD", "BD"): ("c+180", 3),
    ("FL", "DL"): ("c-90", 2),    ("FL", "UL"): ("c+90", 2),    ("FL", "BL"): ("c+180", 3),
    ("BU", "RU"): ("c-90", 2),    ("BU", "LU"): ("c+90", 2),    ("BU", "FU"): ("c+180", 3),
    ("BR", "DR"): ("c-90", 2),    ("BR", "UR"): ("c+90", 2),    ("BR", "FR"): ("c+180", 3),
    ("BD", "LD"): ("c-90", 2),    ("BD", "RD"): ("c+90", 2),    ("BD", "FD"): ("c+180", 3),
    ("BL", "UL"): ("c-90", 2),    ("BL", "DL"): ("c+90", 2),    ("BL", "FL"): ("c+180", 3),
    ("RU", "FU"): ("c-90", 2),    ("RU", "BU"): ("c+90", 2),    ("RU", "LU"): ("c+180", 3),
    ("RF", "DF"): ("c-90", 2),    ("RF", "UF"): ("c+90", 2),    ("RF", "LF"): ("c+180", 3),
    ("RD", "BD"): ("c-90", 2),    ("RD", "FD"): ("c+90", 2),    ("RD", "LD"): ("c+180", 3),
    ("RB", "UB"): ("c-90", 2),    ("RB", "DB"): ("c+90", 2),    ("RB", "LB"): ("c+180", 3),
    ("LU", "BU"): ("c-90", 2),    ("LU", "FU"): ("c+90", 2),    ("LU", "RU"): ("c+180", 3),
    ("LF", "UF"): ("c-90", 2),    ("LF", "DF"): ("c+90", 2),    ("LF", "RF"): ("c+180", 3),
    ("LD", "FD"): ("c-90", 2),    ("LD", "BD"): ("c+90", 2),    ("LD", "RD"): ("c+180", 3),
    ("LB", "DB"): ("c-90", 2),    ("LB", "UB"): ("c+90", 2),    ("LB", "RB"): ("c+180", 3),
}
# ===== NOTASI TAMBAHAN =====

# ==============================================================================
# ## BAGIAN 2: ALGORITMA IDA* (Tidak ada perubahan) ##
# ==============================================================================
best_path = []
min_cost = float('inf')

def search_robot_path(path, g_cost, bound, moves_to_execute):
    global best_path, min_cost
    current_move_idx, current_orientation = path[-1]
    h_cost = len(moves_to_execute) - current_move_idx
    f_cost = g_cost + h_cost
    if f_cost > bound:
        return f_cost
    if h_cost == 0:
        if g_cost < min_cost:
            min_cost = g_cost
            best_path = list(path)
        return g_cost
    next_bound = float('inf')
    move = moves_to_execute[current_move_idx]
    base_move = move[0]
    if base_move in set_H1.get(current_orientation, []):
        path.append((current_move_idx + 1, current_orientation))
        result = search_robot_path(path, g_cost + 1, bound, moves_to_execute)
        if result <= bound: return result
        next_bound = min(next_bound, result)
        path.pop()
    possible_new_orientations = set_I1.get((current_orientation, base_move), [])
    for new_orientation in possible_new_orientations:
        command, cost = re_orient.get((current_orientation, new_orientation), (None, 0))
        if not command: continue
        path.append((current_move_idx + 1, new_orientation))
        result = search_robot_path(path, g_cost + cost, bound, moves_to_execute)
        if result <= bound: return result
        next_bound = min(next_bound, result)
        path.pop()
    return next_bound

def solve_with_ida_robot_optimizer(moves_to_execute, initial_orientation="UF"):
    global best_path, min_cost
    best_path, min_cost = [], float('inf')
    initial_path = [(0, initial_orientation)]
    bound = len(moves_to_execute)
    while True:
        result = search_robot_path(initial_path, 0, bound, moves_to_execute)
        if result <= bound: return best_path
        if result == float('inf'): return None
        bound = result

def reconstruct_script(optimal_path, moves_to_execute):
    robot_commands = []
    if not optimal_path: return []
    for i in range(len(optimal_path) - 1):
        _, old_orientation = optimal_path[i]
        _, new_orientation = optimal_path[i+1]
        if old_orientation != new_orientation:
            command, _ = re_orient.get((old_orientation, new_orientation))
            robot_commands.append(command)
        robot_commands.append(moves_to_execute[i])
    return robot_commands

# ==============================================================================
# ## BAGIAN 3: FUNGSI UTAMA MODUL ( <-- PERUBAHAN UTAMA) ##
# ==============================================================================

def dapatkan_solusi_robot(string_kubus, max_solve_time=10):
    """
    Menerima string kondisi kubus, menyelesaikannya, dan mengoptimalkan untuk robot.
    @param string_kubus: String 54 karakter dari kondisi kubus acak.
    @param max_solve_time: Batas waktu untuk solver Kociemba (detik).
    @return: String perintah akhir untuk robot, atau None jika gagal.
    """
    # TAHAP 1: Dapatkan solusi mentah dari Kociemba
    print("[Solver] Mencari solusi langkah standar menggunakan Kociemba...")
    try:
        raw_solution_str = kociemba_solve(string_kubus, max_length=22, timeout=max_solve_time)
        print(f"[Solver] Solusi mentah ditemukan: {raw_solution_str}")
    except Exception as e:
        print(f"[Solver] Terjadi error saat memanggil Kociemba: {e}")
        return None

    if "Error" in raw_solution_str or not raw_solution_str:
        print("[Solver] Gagal mendapatkan solusi valid dari Kociemba.")
        return None

    # TAHAP 2: Optimalkan solusi untuk gerakan robot
    moves_list = raw_solution_str.split('(')[0].strip().split(' ')
    print("\n[Solver] Mengoptimalkan jalur eksekusi robotik dengan IDA*...")
    start_time = time.time()
    
    optimal_path = solve_with_ida_robot_optimizer(moves_list)
    
    end_time = time.time()
    print(f"[Solver] Pencarian IDA* selesai dalam {end_time - start_time:.4f} detik.")

    if not optimal_path:
        print("[Solver] Gagal menemukan jalur eksekusi robotik yang optimal.")
        return None

    # TAHAP 3: Bangun skrip final
    # ==========================================================
    # ### PERBAIKAN DI SINI ###
    # Menggunakan 'moves_list' yang merupakan nama variabel yang benar
    final_script_list = reconstruct_script(optimal_path, moves_list)
    # ==========================================================
    final_output_string = " ".join(final_script_list)
    
    print(f"[Solver] Skrip robot final berhasil dibuat (Total Biaya: {min_cost}).")
    return final_output_string

# ==============================================================================
# ## BAGIAN 4: BLOK EKSEKUSI (Untuk Testing Mandiri) ##
# ==============================================================================

if __name__ == '__main__':
    print("Menjalankan modul solver secara mandiri untuk pengujian...")
    
    # Gunakan string contoh yang valid untuk pengujian
    test_cube_string = "BBURUDBFUFFFRRFUUFLULUFUDLRRDBBDBDBLUDDFLLRRBRLLLBRDDF"
    print(f"Input string untuk diuji: {test_cube_string}")
    
    final_solution = dapatkan_solusi_robot(test_cube_string)
    
    if final_solution:
        print("\n" + "="*50)
        print("      SKRIP AKHIR UNTUK ROBOT (OUTPUT FINAL)")
        print("="*50)
        print(final_solution)
        print("="*50)
    else:
        print("\nPengujian gagal: Tidak ada solusi yang dihasilkan.")