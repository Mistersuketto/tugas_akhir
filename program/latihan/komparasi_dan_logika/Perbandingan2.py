# program sederhana penggunaan operasi komparasi dan logika

# +++0---5+++8---11+++
print("+++0---5+++8---11+++")
print("====================\n")

# mengambil masukan dari pengguna dan dicasting ke tipe data float
inputUser = float(input("Masukkan angka selain antara 0 - 5 dan 8 - 11: "))

# membandingkan masukan pengguna apakah di antara 0 - 5 atau 8 - 11
komparasi1 = 0 <= inputUser <= 5
komparasi2 = 8 <= inputUser <= 11
logika1 = not komparasi1
logika2 = not komparasi2
hasil = logika1 and logika2

# menampilkan hasil perbandingan
print("Angka yang dimasukkan selain antara 0 - 5 dan 8 - 11:", hasil)