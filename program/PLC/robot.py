import re
import time
from fins import FinsClient
import struct

# ==============================================================================
# FUNGSI BANTU 1: Penerjemah Algoritma (Tidak Diubah)
# Fungsi ini tetap ada dan tidak diubah sama sekali.
# ==============================================================================
def translate_algorithm(input_sequence):
    """
    Menerjemahkan sekuens algoritma kompleks menjadi gerakan dasar robot
    dengan melacak orientasi kubus.
    """
    MOVE_MAP = {
        'U1': 'U', 'U2': 'U2', 'U3': "U'", 'F1': 'F', 'F2': 'F2', 'F3': "F'",
        'D1': 'D', 'D2': 'D2', 'D3': "D'", 'B1': 'B', 'B2': 'B2', 'B3': "B'",
        'R1': 'R', 'R2': 'R2', 'R3': "R'", 'L1': 'L', 'L2': 'L2', 'L3': "L'",
    }
    ORIENTATION_TRANSITIONS = {
        ('UF', 'a+90'): 'FD', ('UF', 'a-90'): 'BU', ('UR', 'a+90'): 'RD', ('UR', 'a-90'): 'LU',
        ('UB', 'a+90'): 'BD', ('UB', 'a-90'): 'FU', ('UL', 'a+90'): 'LD', ('UL', 'a-90'): 'RU',
        ('DF', 'a+90'): 'FU', ('DF', 'a-90'): 'BD', ('DR', 'a+90'): 'RU', ('DR', 'a-90'): 'LD',
        ('DB', 'a+90'): 'BU', ('DB', 'a-90'): 'FD', ('DL', 'a+90'): 'LU', ('DL', 'a-90'): 'RD',
        ('FU', 'a+90'): 'UB', ('FU', 'a-90'): 'DF', ('FR', 'a+90'): 'RB', ('FR', 'a-90'): 'LF',
        ('FD', 'a+90'): 'DB', ('FD', 'a-90'): 'UF', ('FL', 'a+90'): 'LB', ('FL', 'a-90'): 'RF',
        ('BU', 'a+90'): 'UF', ('BU', 'a-90'): 'DB', ('BR', 'a+90'): 'RF', ('BR', 'a-90'): 'LB',
        ('BD', 'a+90'): 'DF', ('BD', 'a-90'): 'UB', ('BL', 'a+90'): 'LF', ('BL', 'a-90'): 'RB',
        ('RU', 'a+90'): 'UL', ('RU', 'a-90'): 'DR', ('RF', 'a+90'): 'FL', ('RF', 'a-90'): 'BR',
        ('RD', 'a+90'): 'DL', ('RD', 'a-90'): 'UR', ('RB', 'a+90'): 'BL', ('RB', 'a-90'): 'FR',
        ('LU', 'a+90'): 'UR', ('LU', 'a-90'): 'DL', ('LF', 'a+90'): 'FR', ('LF', 'a-90'): 'LB',
        ('LD', 'a+90'): 'DR', ('LD', 'a-90'): 'UL', ('LB', 'a+90'): 'BR', ('LB', 'a-90'): 'FL',
        ('UF', 'b+90'): 'UR', ('UF', 'b-90'): 'UL', ('UF', 'b+180'): 'UB', ('UR', 'b+90'): 'UB',
        ('UR', 'b-90'): 'UF', ('UR', 'b+180'): 'UL', ('UB', 'b+90'): 'UL', ('UB', 'b-90'): 'UR',
        ('UB', 'b+180'): 'UF', ('UL', 'b+90'): 'UF', ('UL', 'b-90'): 'UB', ('UL', 'b+180'): 'UR',
        ('DF', 'b+90'): 'DL', ('DF', 'b-90'): 'DR', ('DF', 'b+180'): 'DB', ('DR', 'b+90'): 'DF',
        ('DR', 'b-90'): 'DB', ('DR', 'b+180'): 'DL', ('DB', 'b+90'): 'DR', ('DB', 'b-90'): 'DL',
        ('DB', 'b+180'): 'DF', ('DL', 'b+90'): 'DB', ('DL', 'b-90'): 'DF', ('DL', 'b+180'): 'DR',
        ('FU', 'b+90'): 'FL', ('FU', 'b-90'): 'FR', ('FU', 'b+180'): 'FD', ('FR', 'b+90'): 'FU',
        ('FR', 'b-90'): 'FD', ('FR', 'b+180'): 'FL', ('FD', 'b+90'): 'FR', ('FD', 'b-90'): 'FL',
        ('FD', 'b+180'): 'FU', ('FL', 'b+90'): 'FD', ('FL', 'b-90'): 'FU', ('FL', 'b+180'): 'FR',
        ('BU', 'b+90'): 'BR', ('BU', 'b-90'): 'BL', ('BU', 'b+180'): 'BD', ('BR', 'b+90'): 'BD',
        ('BR', 'b-90'): 'BU', ('BR', 'b+180'): 'BL', ('BD', 'b+90'): 'BL', ('BD', 'b-90'): 'BR',
        ('BD', 'b+180'): 'BU', ('BL', 'b+90'): 'BU', ('BL', 'b-90'): 'BD', ('BL', 'b+180'): 'BR',
        ('RU', 'b+90'): 'RF', ('RU', 'b-90'): 'RB', ('RU', 'b+180'): 'RD', ('RF', 'b+90'): 'RD',
        ('RF', 'b-90'): 'RU', ('RF', 'b+180'): 'RB', ('RD', 'b+90'): 'RB', ('RD', 'b-90'): 'RF',
        ('RD', 'b+180'): 'RU', ('RB', 'b+90'): 'RU', ('RB', 'b-90'): 'RD', ('RB', 'b+180'): 'RF',
        ('LU', 'b+90'): 'LB', ('LU', 'b-90'): 'LF', ('LU', 'b+180'): 'LD', ('LF', 'b+90'): 'LU',
        ('LF', 'b-90'): 'LD', ('LF', 'b+180'): 'LB', ('LD', 'b+90'): 'LF', ('LD', 'b-90'): 'LB',
        ('LD', 'b+180'): 'LU', ('LB', 'b+90'): 'LD', ('LB', 'b-90'): 'LU', ('LB', 'b+180'): 'LF',
        ('UF', 'c-90'): 'RF', ('UF', 'c+90'): 'LF', ('UF', 'c+180'): 'DF', ('UR', 'c-90'): 'BR',
        ('UR', 'c+90'): 'FR', ('UR', 'c+180'): 'DR', ('UB', 'c-90'): 'LB', ('UB', 'c+90'): 'RB',
        ('UB', 'c+180'): 'DB', ('UL', 'c-90'): 'FL', ('UL', 'c+90'): 'BL', ('UL', 'c+180'): 'DL',
        ('DF', 'c-90'): 'LF', ('DF', 'c+90'): 'RF', ('DF', 'c+180'): 'UF', ('DR', 'c-90'): 'FR',
        ('DR', 'c+90'): 'BR', ('DR', 'c+180'): 'UR', ('DB', 'c-90'): 'RB', ('DB', 'c+90'): 'LB',
        ('DB', 'c+180'): 'UB', ('DL', 'c-90'): 'BL', ('DL', 'c+90'): 'FL', ('DL', 'c+180'): 'UL',
        ('FU', 'c-90'): 'LU', ('FU', 'c+90'): 'RU', ('FU', 'c+180'): 'BU', ('FR', 'c-90'): 'UR',
        ('FR', 'c+90'): 'DR', ('FR', 'c+180'): 'BR', ('FD', 'c-90'): 'RD', ('FD', 'c+90'): 'LD',
        ('FD', 'c+180'): 'BD', ('FL', 'c-90'): 'DL', ('FL', 'c+90'): 'UL', ('FL', 'c+180'): 'BL',
        ('BU', 'c-90'): 'RU', ('BU', 'c+90'): 'LU', ('BU', 'c+180'): 'FU', ('BR', 'c-90'): 'DR',
        ('BR', 'c+90'): 'UR', ('BR', 'c+180'): 'FR', ('BD', 'c-90'): 'LD', ('BD', 'c+90'): 'RD',
        ('BD', 'c+180'): 'FD', ('BL', 'c-90'): 'UL', ('BL', 'c+90'): 'DL', ('BL', 'c+180'): 'FL',
        ('RU', 'c-90'): 'FU', ('RU', 'c+90'): 'BU', ('RU', 'c+180'): 'LU', ('RF', 'c-90'): 'DF',
        ('RF', 'c+90'): 'UF', ('RF', 'c+180'): 'LF', ('RD', 'c-90'): 'BD', ('RD', 'c+90'): 'FD',
        ('RD', 'c+180'): 'LD', ('RB', 'c-90'): 'UB', ('RB', 'c+90'): 'DB', ('RB', 'c+180'): 'LB',
        ('LU', 'c-90'): 'BU', ('LU', 'c+90'): 'FU', ('LU', 'c+180'): 'RU', ('LF', 'c-90'): 'UF',
        ('LF', 'c+90'): 'DF', ('LF', 'c+180'): 'RF', ('LD', 'c-90'): 'FD', ('LD', 'c+90'): 'BD',
        ('LD', 'c+180'): 'RD', ('LB', 'c-90'): 'DB', ('LB', 'c+90'): 'UB', ('LB', 'c+180'): 'RB',
    }
    FACE_POSITIONS = {
        'UF': {'U_pos': 'U', 'F_pos': 'F'}, 'UR': {'U_pos': 'U', 'F_pos': 'R'},
        'UB': {'U_pos': 'U', 'F_pos': 'B'}, 'UL': {'U_pos': 'U', 'F_pos': 'L'},
        'DF': {'U_pos': 'D', 'F_pos': 'F'}, 'DR': {'U_pos': 'D', 'F_pos': 'R'},
        'DB': {'U_pos': 'D', 'F_pos': 'B'}, 'DL': {'U_pos': 'D', 'F_pos': 'L'},
        'FU': {'U_pos': 'F', 'F_pos': 'U'}, 'FR': {'U_pos': 'F', 'F_pos': 'R'},
        'FD': {'U_pos': 'F', 'F_pos': 'D'}, 'FL': {'U_pos': 'F', 'F_pos': 'L'},
        'BU': {'U_pos': 'B', 'F_pos': 'U'}, 'BR': {'U_pos': 'B', 'F_pos': 'R'},
        'BD': {'U_pos': 'B', 'F_pos': 'D'}, 'BL': {'U_pos': 'B', 'F_pos': 'L'},
        'RU': {'U_pos': 'R', 'F_pos': 'U'}, 'RF': {'U_pos': 'R', 'F_pos': 'F'},
        'RD': {'U_pos': 'R', 'F_pos': 'D'}, 'RB': {'U_pos': 'R', 'F_pos': 'B'},
        'LU': {'U_pos': 'L', 'F_pos': 'U'}, 'LF': {'U_pos': 'L', 'F_pos': 'F'},
        'LD': {'U_pos': 'L', 'F_pos': 'D'}, 'LB': {'U_pos': 'L', 'F_pos': 'B'},
    }
    moves = re.findall(r'[A-Z]\d|[abc][+-]\d+', input_sequence)
    current_orientation, translated_moves = "UF", []
    print("\n[PLC-Translator] Memulai proses penerjemahan langkah-demi-langkah...")
    for i, move_code in enumerate(moves):
        robot_move = None
        if move_code[0] in ['a', 'b', 'c']:
            robot_move = move_code
            new_orientation = ORIENTATION_TRANSITIONS.get((current_orientation, robot_move))
            if new_orientation:
                print(f"  {i+1}. Langkah '{move_code}': Rotasi kubus. Orientasi berubah dari {current_orientation} -> {new_orientation}")
                current_orientation = new_orientation
            else: print(f"  Peringatan: Transisi dari '{current_orientation}' dengan '{robot_move}' belum terdefinisi.")
        else:
            standard_move = MOVE_MAP.get(move_code)
            if not standard_move: continue
            required_face = standard_move[0]
            positions = FACE_POSITIONS.get(current_orientation)
            if not positions: continue
            if positions['U_pos'] == required_face: robot_move = 'U' + (standard_move[1:] if len(standard_move) > 1 else '')
            elif positions['F_pos'] == required_face: robot_move = 'F' + (standard_move[1:] if len(standard_move) > 1 else '')
            else: robot_move = f"[ERROR: {required_face} tidak terjangkau]"
            print(f"  {i+1}. Langkah '{standard_move}': Orientasi '{current_orientation}'. Gerakan robot -> '{robot_move}'")
        if robot_move: translated_moves.append(robot_move)
    return " ".join(translated_moves)

# ==============================================================================
# FUNGSI BANTU 2: Eksekusi PLC (Sedikit Diubah untuk Mengembalikan Status)
# ==============================================================================
def execute_on_plc(robot_script, plc_host):
    """Mengeksekusi skrip yang sudah diterjemahkan ke hardware PLC."""
    ROBOT_MOVE_TO_PLC_ADDRESS = {
        "U": "CIO10.0",     "U2": "CIO10.1",    "U'": "CIO10.2",
        "F": "CIO10.3",     "F2": "CIO10.4",    "F'": "CIO10.5",
        "a+90": "CIO10.6",  "a-90": "CIO10.7",  "b+90": "CIO10.8",      "b+180": "CIO10.9",
        "b-90": "CIO10.10", "c+90": "CIO10.12", "c+180": "CIO10.13",    "c-90": "CIO10.14",
    }
    FEEDBACK_ADDRESS = "D0"
    moves_to_execute = robot_script.strip().split(' ')
    if not moves_to_execute or moves_to_execute == ['']: return True
    client = None
    try:
        print(f"\n[PLC-Executor] Mencoba terhubung ke PLC di {plc_host}...")
        client = FinsClient(host=plc_host); client.connect()
        print(f"[PLC-Executor] ✅ Berhasil terhubung.")
        client.memory_area_write(FEEDBACK_ADDRESS, b"\x00\x00")
        for i, move in enumerate(moves_to_execute):
            print(f"\n--- Eksekusi Langkah {i+1}/{len(moves_to_execute)}: '{move}' ---")
            command_address = ROBOT_MOVE_TO_PLC_ADDRESS.get(move)
            if not command_address:
                print(f"⚠️  Peringatan: Gerakan '{move}' tidak memiliki alamat PLC. Melewati..."); continue
            client.memory_area_write(command_address, b"\x01")
            print(f"  -> Perintah dikirim ke {command_address}")
            print(f"  -> Menunggu {FEEDBACK_ADDRESS} siap (nilai 0)...")
            while True:
                if struct.unpack('>H', client.memory_area_read(FEEDBACK_ADDRESS, 1).data)[0] == 0: break
                time.sleep(0.1)
            print(f"  -> Menunggu konfirmasi ({FEEDBACK_ADDRESS} menjadi 1)...")
            while True:
                if struct.unpack('>H', client.memory_area_read(FEEDBACK_ADDRESS, 1).data)[0] == 1:
                    print(f"  -> Konfirmasi diterima!"); break
                time.sleep(0.1)
            client.memory_area_write(command_address, b"\x00")
        print("\n[PLC-Executor] ✅ Semua langkah berhasil dieksekusi!")
        return True
    except Exception as e:
        print(f"\n[PLC-Executor] ❌ Terjadi kesalahan: {e}"); return False
    finally:
        if client: client.close(); print("[PLC-Executor] 🔌 Koneksi ditutup.")

# ==============================================================================
# FUNGSI UTAMA MODUL (Ini yang akan dipanggil oleh main.py)
# ==============================================================================
def jalankan_penerjemah_dan_plc(optimal_script, plc_host="192.168.1.28"):
    """
    Fungsi utama yang mengorkestrasi penerjemahan dan eksekusi PLC.
    Menerima skrip dari modul algorithm dan menjalankannya di hardware.
    """
    # 1. Panggil fungsi penerjemah untuk mendapatkan skrip bersih untuk robot
    final_robot_script = translate_algorithm(optimal_script)
    
    print("\n" + "="*50)
    print("           HASIL AKHIR PENERJEMAHAN UNTUK PLC")
    print("="*50)
    print(f"Input Optimal     : {optimal_script}")
    print(f"Hasil Terjemahan  : {final_robot_script}")
    print("="*50)
    
    # 2. Panggil fungsi eksekusi dengan hasil terjemahan
    if final_robot_script:
        return execute_on_plc(final_robot_script, plc_host)
    else:
        print("[PLC] Tidak ada skrip yang valid untuk dieksekusi.")
        return False

# ==============================================================================
# BLOK EKSEKUSI (Untuk Testing Mandiri)
# ==============================================================================
if __name__ == "__main__":
    print(">>> Menjalankan modul PLC & Translator secara mandiri untuk pengujian...")
    # Contoh input yang seharusnya datang dari modul algorithm.py
    test_input = "U3 c-90 R1 c-90 D2"
    jalankan_penerjemah_dan_plc(test_input)