import sys
import os
import time

# ==============================================================================
# ## BAGIAN 1: KONFIGURASI, PUSTAKA, DAN PENGETAHUAN ROBOT ##
# ==============================================================================

# --- Pengaturan Path dan Impor Pustaka Kociemba Standar ---
SOLVER_FOLDER_NAME = 'RubiksCube-TwophaseSolver'
project_path = os.path.abspath(SOLVER_FOLDER_NAME)
if project_path not in sys.path:
    sys.path.append(project_path)

try:
    from solver import solve as kociemba_solve
except ImportError:
    print(f"Error: Tidak dapat menemukan pustaka di folder '{SOLVER_FOLDER_NAME}'.")
    sys.exit(1)

# --- Definisi Notasi Gerakan Robot Anda ---
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
# ## BAGIAN 2: ALGORITMA IDA* UNTUK OPTIMISASI ROBOTIK ##
# ==============================================================================

# Variabel global untuk menyimpan solusi terbaik dari IDA*
best_path = []
min_cost = float('inf')

def search_robot_path(path, g_cost, bound, moves_to_execute):
    """Fungsi pencarian rekursif IDA* untuk menemukan jalur eksekusi termurah."""
    global best_path, min_cost

    # Ambil state saat ini dari path
    current_move_idx, current_orientation = path[-1]

    # Heuristik h(n) = jumlah langkah tersisa (setiap langkah minimal berbobot 1)
    h_cost = len(moves_to_execute) - current_move_idx
    
    # Fungsi evaluasi f(n) = g(n) + h(n)
    f_cost = g_cost + h_cost

    if f_cost > bound:
        return f_cost
    
    # Jika kita sudah mengeksekusi semua langkah, kita menemukan solusi
    if h_cost == 0:
        if g_cost < min_cost:
            min_cost = g_cost
            best_path = list(path)
        return g_cost

    next_bound = float('inf')

    # Tentukan gerakan selanjutnya yang harus dieksekusi
    move = moves_to_execute[current_move_idx]
    base_move = move[0]

    # Opsi 1: Gerakan bisa dieksekusi langsung (Aksi Set H1)
    if base_move in set_H1.get(current_orientation, []):
        path.append((current_move_idx + 1, current_orientation))
        result = search_robot_path(path, g_cost + 1, bound, moves_to_execute)
        if result <= bound: return result
        next_bound = min(next_bound, result)
        path.pop()
    
    # Opsi 2: Gerakan memerlukan re-orientasi (Aksi Set I1)
    # Loop melalui semua kemungkinan orientasi baru
    possible_new_orientations = set_I1.get((current_orientation, base_move), [])
    for new_orientation in possible_new_orientations:
        # Cari perintah dan bobotnya di kamus re_orient
        command, cost = re_orient.get((current_orientation, new_orientation), (None, 0))
        if not command: continue # Lewati jika transisi tidak terdefinisi

        path.append((current_move_idx + 1, new_orientation))
        result = search_robot_path(path, g_cost + cost, bound, moves_to_execute)
        if result <= bound: return result
        next_bound = min(next_bound, result)
        path.pop()

    return next_bound


def solve_with_ida_robot_optimizer(moves_to_execute, initial_orientation="UF"):
    """Driver loop IDA* untuk menjalankan pencarian."""
    global best_path, min_cost
    best_path = []
    min_cost = float('inf')

    # State awal: (langkah ke-0, orientasi awal)
    initial_path = [(0, initial_orientation)]
    
    # Bound awal adalah heuristik dari state awal
    bound = len(moves_to_execute)

    while True:
        result = search_robot_path(initial_path, 0, bound, moves_to_execute)
        if result <= bound:
            return best_path # Solusi ditemukan
        if result == float('inf'):
            return None # Tidak ada solusi
        bound = result # Tingkatkan bound ke nilai berikutnya

def reconstruct_script(optimal_path, moves_to_execute):
    """Membangun daftar perintah akhir dari path optimal yang ditemukan IDA*."""
    robot_commands = []
    if not optimal_path: return []
    
    for i in range(len(optimal_path) - 1):
        _, old_orientation = optimal_path[i]
        _, new_orientation = optimal_path[i+1]
        
        # Jika orientasi berubah, tambahkan perintah re-orientasi
        if old_orientation != new_orientation:
            command, _ = re_orient.get((old_orientation, new_orientation))
            robot_commands.append(command)
            
        # Tambahkan perintah putaran muka
        robot_commands.append(moves_to_execute[i])
        
    return robot_commands


# ==============================================================================
# ## BAGIAN 3: ALUR UTAMA PROGRAM ##
# ==============================================================================

if __name__ == "__main__":
    # 1. Input: 54-char string dari kubus acak
    scrambled_cube_string = "UUUBUUBRFDBBRRULDRLBLLFFDDFFFUFDRBDUBLDLLFRURLLRRBDFBD"

    # --- TAHAP 1: DAPATKAN SOLUSI CEPAT ---
    print("[Tahap 1] Mencari solusi langkah standar...")
    raw_solution_str = kociemba_solve(scrambled_cube_string, max_length=22, timeout=10)
    print(f"Solusi mentah Kociemba ditemukan: {raw_solution_str}")

    if "Error" not in raw_solution_str and raw_solution_str:
        # Bersihkan solusi menjadi daftar gerakan
        moves_list = raw_solution_str.split('(')[0].strip().split(' ')
        
        # --- TAHAP 2: OPTIMISASI DENGAN IDA* ROBOTIK ---
        print("\n[Tahap 2] Mencari jalur eksekusi robotik termurah dengan IDA*...")
        start_time = time.time()
        optimal_path = solve_with_ida_robot_optimizer(moves_list)
        end_time = time.time()
        print(f"Pencarian IDA* selesai dalam {end_time - start_time:.4f} detik.")

        if optimal_path:
            # Bangun skrip akhir dari path optimal
            final_script_list = reconstruct_script(optimal_path, moves_list)
            final_output_string = " ".join(final_script_list)

            # --- HASIL AKHIR ---
            print("\n" + "="*50)
            print("      SKRIP AKHIR UNTUK ROBOT (OUTPUT FINAL)")
            print("="*50)
            print(final_output_string)
            print(f"(Total Biaya Terendah: {min_cost})")
            print("="*50)
        else:
            print("Tidak dapat menemukan jalur eksekusi robotik yang optimal.")
    else:
        print("\nTidak dapat melanjutkan ke Tahap 2 karena solusi awal tidak valid atau tidak ditemukan.")