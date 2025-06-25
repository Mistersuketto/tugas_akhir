# program sederhana penggunaan operasi komparasi dan logika

# ---0+++5---8+++11---
print("---0+++5---8+++11---")
print("====================\n")

# mengambil masukan dari pengguna dan dicasting ke tipe data float
inputUser = float(input("Masukkan angka antara 0 - 5 atau 8 - 11: "))

# membandingkan masukan pengguna apakah di antara 0 - 5 atau 8 - 11
komparasi1 = 0 < inputUser < 5
komparasi2 = 8 < inputUser < 11
hasil = komparasi1 or komparasi2

# menampilkan hasil perbandingan
print("Angka yang dimasukkan di antara 0 - 5 atau 8 - 11:", hasil)