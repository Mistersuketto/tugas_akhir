from pymodbus.client import ModbusTcpClient
import time

ip_plc = '192.168.1.28'
port_plc = 9600

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
