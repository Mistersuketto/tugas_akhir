# program sederhana penggunaan casting tipe data dan input user

print("Konversi Suhu Kelvin")
print("====================\n")

# casting tipe data dari input user
suhuK = float(input("Masukkan Suhu dalam Kelvin = "))

# proses konversi suhu kelvin ke suhu celcius
suhuC = suhuK - 273
print("Suhu dalam Celcius =", suhuC)

# proses konversi suhu kelvin ke suhu reamur
suhuR = (4 / 5) * (suhuK - 273)
print("Suhu dalam Reamur =", suhuR)

# proses konversi suhu kelvin ke suhu fahrenheit
suhuF = ((9 / 5) * (suhuK - 273)) + 32
print("Suhu dalam Fahrenheit =", suhuF)