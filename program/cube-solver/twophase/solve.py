import time

from .cubes import CoordCube, FaceCube
from .pieces import Color
from .tables import Tables

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

class SolutionManager:
    def __init__(self, facelets):
        """
        A utility class for managing the search for the solution.

        Parameters
        ----------
        facelets: str
            Starting position of the cube. Should be a 54 character string
            specifying the stickers on each face (in order U R F D L B),
            reading row by row from the top left hand corner to the bottom
            right
        """
        self.tables = Tables()

        self.facelets = facelets.upper()

        status = self.verify()
        if status:
            error_message = {
                -1: "each colour should appear exactly 9 times",
                -2: "not all edges exist exactly once",
                -3: "one edge should be flipped",
                -4: "not all corners exist exactly once",
                -5: "one corner should be twisted",
                -6: "two corners or edges should be exchanged",
            }
            raise ValueError("Invalid cube: {}".format(error_message[status]))

    def solve(self, max_length=25, timeout=float("inf")):
        """
        Solve the cube.

        This method implements back to back IDA* searches for phase 1 and phase
        2, returning the result. Can be called multiple times with decreasing
        max_length to try and find better solutions.

        Parameters
        ----------
        max_length: int, optional
            Upper bound for the allowed number of moves.
        max_time: int or float, optional
            Time at which to quit searching. Algorithm will quit when
            ``time.time() > max_time``.
        """
        # prepare for phase 1
        self._phase_1_initialise(max_length)
        self._allowed_length = max_length
        self._timeout = timeout

        for bound in range(self._allowed_length):
            n = self._phase_1_search(0, bound)
            if n >= 0:
                # solution found
                return self._solution_to_string(n)
            elif n == -2:
                # time limit exceeded
                return -2

        # no solution found
        return -1

    def verify(self):
        count = [0] * 6
        try:
            for char in self.facelets:
                count[Color[char]] += 1
        except (IndexError, ValueError):
            return -1
        for i in range(6):
            if count[i] != 9:
                return -1

        fc = FaceCube(self.facelets)
        cc = fc.to_cubiecube()

        return cc.verify()

    def _phase_1_initialise(self, max_length):
        # the lists 'axis' and 'power' will store the nth move (index of face
        # being turned stored in axis, number of clockwise quarter turns stored
        # in power). The nth move is stored in position n-1
        self.axis = [0] * max_length
        self.power = [0] * max_length

        # ===== TRACK KONDISI RUBIK DAN BIAYA =====
        self.robotic_cost = [0] * max_length
        self.orientation = [""] * max_length
        # ===== TRACK KONDISI RUBIK DAN BIAYA =====

        # the lists twist, flip and udslice store the phase 1 coordinates after
        # n moves. position 0 stores the initial states, the coordinates after n
        # moves are stored in position n
        self.twist = [0] * max_length
        self.flip = [0] * max_length
        self.udslice = [0] * max_length

        # similarly to above, these lists store the phase 2 coordinates after n
        # moves.
        self.corner = [0] * max_length
        self.edge4 = [0] * max_length
        self.edge8 = [0] * max_length

        # the following two arrays store minimum number of moves required to
        # reach phase 2 or a solution respectively
        # after n moves. these estimates come from the pruning tables and are
        # used to exclude branches in the search tree.
        self.min_dist_1 = [0] * max_length
        self.min_dist_2 = [0] * max_length

        # initialise the arrays from the input
        self.f = FaceCube(self.facelets)
        self.c = CoordCube.from_cubiecube(self.f.to_cubiecube())
        self.twist[0] = self.c.twist
        self.flip[0] = self.c.flip
        self.udslice[0] = self.c.udslice
        self.corner[0] = self.c.corner
        self.edge4[0] = self.c.edge4
        self.edge8[0] = self.c.edge8

        # ===== INISIALISASI KONDISI RUBIK DAN BIAYA =====
        self.robotic_cost[0] = 0
        self.orientation[0] = "UF"
        # ===== INISIALISASI KONDISI RUBIK DAN BIAYA =====
        
        self.min_dist_1[0] = self._phase_1_cost(0)

    def _phase_2_initialise(self, n):
        if time.time() > self._timeout:
            return -2
        # initialise phase 2 search from the phase 1 solution
        cc = self.f.to_cubiecube()
        for i in range(n):
            for j in range(self.power[i]):
                cc.move(self.axis[i])
        self.edge4[n] = cc.edge4
        self.edge8[n] = cc.edge8
        self.corner[n] = cc.corner
        
        # Dapatkan biaya yang sudah dihabiskan di Fase 1
        phase1_cost = self.robotic_cost[n]
        
        # Loop ini sekarang mengiterasi 'added_bound', yaitu tambahan anggaran biaya untuk Fase 2
        # Kita mulai dari heuristik Fase 2 hingga sisa anggaran yang tersedia
        start_bound = self._phase_2_cost(n)
        for added_bound in range(start_bound, self._allowed_length - phase1_cost + 1):
            total_bound = phase1_cost + added_bound
            # Panggil pencarian Fase 2 dengan total_bound
            m = self._phase_2_search(n, total_bound)
            if m >= 0:
                return m

        return -1

    def _phase_1_cost(self, n):
        """
        Cost of current position for use in phase 1. Returns a lower bound on
        the number of moves requires to get to phase 2.
        """
        return max(
            self.tables.udslice_twist_prune[self.udslice[n], self.twist[n]],
            self.tables.udslice_flip_prune[self.udslice[n], self.flip[n]],
        )

    def _phase_2_cost(self, n):
        """
        Cost of current position for use in phase 2. Returns a lower bound on
        the number of moves required to get to a solved cube.
        """
        return max(
            self.tables.edge4_corner_prune[self.edge4[n], self.corner[n]],
            self.tables.edge4_edge8_prune[self.edge4[n], self.edge8[n]],
        )

    def _phase_1_search(self, n, bound):
        if time.time() > self._timeout:
            return -2
        
        # ===== MODIFIKASI =====
        current_robotic_cost = self.robotic_cost[n]
        current_orientation = self.orientation[n]

        # Hitung f(n) = g(n) + h(n)
        # g(n) sekarang adalah biaya robotik kita, bukan lagi jumlah langkah 'n'
        # h(n) tetap sama, yaitu estimasi dari pruning table
        h_cost = self._phase_1_cost(n)
        f_cost = current_robotic_cost + h_cost

        # Jika f_cost melebihi batas, pangkas cabang ini.
        # Ini adalah jantung dari algoritma A* / IDA*.
        if f_cost > bound:
            return -1  # Kembalikan -1 untuk menandakan tidak ada solusi di jalur ini

        # Jika h_cost == 0, berarti tujuan Fase 1 tercapai.
        if h_cost == 0:
            return self._phase_2_initialise(n)
        
        # Loop melalui semua kemungkinan gerakan (6 sisi x 3 putaran)
        for i in range(6):
            # Logika untuk tidak memutar sisi yang sama/berlawanan secara berurutan tetap sama
            if n > 0 and self.axis[n - 1] in (i, i + 3):
                continue

            for j in range(1, 4):
                # Tentukan karakter gerakan (misal, 'U', 'R', 'F') dari indeks numerik 'i'
                move_char = Color(i).name

                # Tentukan biaya dan orientasi selanjutnya berdasarkan aturan robot
                cost_of_this_move = 0
                next_orientation = current_orientation

                # Cek apakah gerakan ada di Set H1 untuk orientasi saat ini
                if move_char in set_H1.get(current_orientation, []):
                    cost_of_this_move = 1
                else: # Jika tidak, berarti gerakan ini memerlukan re-orientasi dari Set I1
                    cost_of_this_move = 2
                    # Dapatkan orientasi baru dari kamus aturan I1_MAP
                    next_orientation = set_I1.get((current_orientation, move_char), current_orientation)

                # Hitung total biaya robotik baru dan simpan ke 'memori'
                new_robotic_cost = current_robotic_cost + cost_of_this_move
                self.robotic_cost[n + 1] = new_robotic_cost
                self.orientation[n + 1] = next_orientation
                self.axis[n] = i
                self.power[n] = j

                mv = 3 * i + j - 1

                # update coordinates
                self.twist[n + 1] = self.tables.twist_move[self.twist[n]][mv]
                self.flip[n + 1] = self.tables.flip_move[self.flip[n]][mv]
                self.udslice[n + 1] = self.tables.udslice_move[self.udslice[n]][mv]

                self.min_dist_1[n + 1] = self._phase_1_cost(n + 1)

                # start search from next node
                # m = self._phase_1_search(n + 1, depth - 1)
                m = self._phase_1_search(n + 1, bound)
                if m >= 0:
                    return m
                if m == -2:
                    # time limit exceeded
                    return -2
        # if no solution found at current depth, return -1
        return -1
    
    def _phase_2_search(self, n, bound):
        # Pengecekan timeout
        if time.time() > self._timeout:
            return -1
        
        # Ambil biaya dan orientasi saat ini
        current_robotic_cost = self.robotic_cost[n]
        current_orientation = self.orientation[n]

        # Hitung f(n) = g(n) + h(n)
        h_cost = self._phase_2_cost(n)
        f_cost = current_robotic_cost + h_cost

        # Pruning berdasarkan bound
        if f_cost > bound:
            return -1

        # Jika h_cost == 0, tujuan akhir (kubus selesai) tercapai!
        if h_cost == 0:
            return n # Kembalikan panjang solusi 'n'

        # Loop melalui gerakan yang diizinkan di Fase 2
        for i in range(6):
            if n > 0 and self.axis[n - 1] in (i, i + 3):
                continue

            for j in range(1, 4):
                # Di Fase 2, beberapa gerakan dibatasi (hanya putaran 180 derajat)
                if i in [1, 2, 4, 5] and j != 2: # R, F, L, B
                    continue

                # === BLOK LOGIKA ROBOTIK (SAMA SEPERTI FASE 1) ===
                move_char = Color(i).name
                
                cost_of_this_move = 0
                next_orientation = current_orientation

                if move_char in set_H1.get(current_orientation, []):
                    cost_of_this_move = 1
                else:
                    cost_of_this_move = 2
                    next_orientation = set_I1.get((current_orientation, move_char), current_orientation)

                new_robotic_cost = current_robotic_cost + cost_of_this_move
                self.robotic_cost[n + 1] = new_robotic_cost
                self.orientation[n + 1] = next_orientation
                # === AKHIR BLOK LOGIKA ROBOTIK ===

                # Simpan detail gerakan
                self.axis[n] = i
                self.power[n] = j

                # Update koordinat Fase 2
                mv = 3 * i + j - 1
                self.edge4[n + 1] = self.tables.edge4_move[self.edge4[n]][mv]
                self.edge8[n + 1] = self.tables.edge8_move[self.edge8[n]][mv]
                self.corner[n + 1] = self.tables.corner_move[self.corner[n]][mv]

                # Hitung heuristik baru
                self.min_dist_2[n + 1] = self._phase_2_cost(n + 1)

                # Panggil rekursif dengan 'bound' yang sama
                m = self._phase_2_search(n + 1, bound)
                if m >= 0:
                    return m
        # if no moves lead to a tree with a solution or min_dist_2 > depth then
        # we return -1 to signify lack of solution
        return -1

    def _solution_to_string(self, length):
        """
        Generate solution string. Uses standard cube notation: F means
        clockwise quarter turn of the F face, U' means a counter clockwise
        quarter turn of the U face, R2 means a half turn of the R face etc.
        """

        def recover_move(axis_power):
            axis, power = axis_power
            if power == 1:
                return Color(axis).name
            if power == 2:
                return Color(axis).name + "2"
            if power == 3:
                return Color(axis).name + "'"
            raise RuntimeError("Invalid move in solution.")

        solution = map(
            recover_move, zip(self.axis[:length], self.power[:length])
        )
        return " ".join(solution)