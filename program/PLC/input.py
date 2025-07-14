import time
import omronfins.finsudp as finsudp
from omronfins.finsudp import datadef

# Inisialisasi FINS UDP Client
# Argumen kedua adalah nomor node dari PC kita, bisa disesuaikan.
fins = finsudp.FinsUDP(0, 170) 

# Buka koneksi ke alamat IP PLC dengan port FINS (9600)
try:
    ret = fins.open('192.168.1.28', 9600)
    if ret:
        print("✅ Koneksi UDP ke PLC berhasil.")
    else:
        print("❌ Gagal membuka koneksi. Pastikan IP dan port sudah benar.")
        exit()

    # Tentukan alamat FINS dari PLC tujuan
    # dst_node_num biasanya adalah digit terakhir dari alamat IP PLC
    fins.set_destination(dst_net_addr=0, dst_node_num=28, dst_unit_addr=0)

    # --- MENYALAKAN COIL 10.00 (SET TO ON) ---
    print("\nMenyalakan Coil 10.00...")
    # Gunakan area memori CIO_BIT
    # Alamat 10.00 -> address=10, bit_offset=0
    # Nilai 1 untuk ON
    ret_on = fins.write_mem_area(datadef.CIO_BIT, 10, 0, 1, [(1, datadef.BIT)])
    if ret_on:
        print("👍 Coil 10.00 berhasil dinyalakan.")
    else:
        print("👎 Gagal menyalakan coil.")

    # Beri jeda 3 detik
    print("Menunggu 3 detik...")
    time.sleep(3)

    # --- MEMATIKAN COIL 10.00 (SET TO OFF) ---
    print("\nMematikan Coil 10.00...")
    # Gunakan area memori dan alamat yang sama
    # Nilai 0 untuk OFF
    ret_off = fins.write_mem_area(datadef.CIO_BIT, 10, 0, 1, [(0, datadef.BIT)])
    if ret_off:
        print("👍 Coil 10.00 berhasil dimatikan.")
    else:
        print("👎 Gagal mematikan coil.")

except Exception as e:
    print(f"Terjadi error: {e}")

finally:
    # Selalu tutup koneksi
    fins.close()
    print("\nKoneksi ditutup.")