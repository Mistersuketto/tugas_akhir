from pymodbus.client import ModbusTcpClient
import time

ip_plc = '192.168.10.16'
port_plc = 502

write_address = 100
read_address = 200

plc = ModbusTcpClient(ip_plc, port=port_plc)

try:
    konek = plc.connect()
    
    if konek:
        print("Koneksi ke PLC berhasil")
    else:
        print("Koneksi ke PLC gagal")
        exit()

finally:
    plc.close()    