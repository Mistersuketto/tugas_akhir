# program sederhana penggunaan casting tipe data dan input user

print("Konversi Suhu Reamur")
print("====================\n")

# casting tipe data dari input user
suhuR = float(input("Masukkan Suhu dalam Reamur = "))

# proses konversi suhu reamur ke suhu celcius
suhuC = (5 / 4) * suhuR
print("Suhu dalam Celcius =", suhuC)

# proses konversi suhu reamur ke suhu fahrenheit
suhuF = ((9 / 4) * suhuR) + 32
print("Suhu dalam Fahrenheit =", suhuF)

# proses konversi suhu reamur ke suhu kelvin
suhuK = ((5 / 4) * suhuR) + 273
print("Suhu dalam Celcius =", suhuK)