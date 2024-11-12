# program sederhana penggunaan casting tipe data dan input user

print("Konversi Suhu Fahrenheit")
print("========================\n")

# casting tipe data dari input user
suhuF = float(input("Masukkan Suhu dalam Fahrenheit = "))

# proses konversi suhu fahrenheit ke suhu celcius
suhuC = (5 / 9) * (suhuF - 32)
print("Suhu dalam Celcius =", suhuC)

# proses konversi suhu fahrenheit ke suhu reamur
suhuR = (4 / 9) * (suhuF - 32)
print("Suhu dalam Fahrenheit =", suhuR)

# proses konversi suhu fahrenheit ke suhu kelvin
suhuK = ((5 / 9) * (suhuF - 32)) + 273
print("Suhu dalam Kelvin =", suhuK)