def format_money(value):
    return "Rp" + format(value, ",.2f")


def read_float(prompt, minimum=0):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Input harus berupa angka.")
            continue

        if value < minimum:
            print(f"Input tidak boleh kurang dari {minimum}.")
            continue

        return value


def read_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Input bukanlah nomor!")


def read_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("y", "ya"):
            return True

        if answer in ("n", "no", "tidak"):
            return False

        print("Jawab dengan y/ya atau n/tidak.")

def main():
    saldo = 0
    investment_plan = []

    while True:
        if saldo > 0:
            print(
                """
Menu Utama
1. Masukkan atau ubah uang awal
2. Tambah investment plan
3. Tambah kebiasaan
4. Lihat profil dan kebiasaan
5. Buka timeline opportunity cost
6. Hapus semua kebiasaan
7. Buka toko barang sekali beli
0. Keluar
"""
            )
        else:
            print(
                """
Menu Utama
1. Masukkan atau ubah uang awal
0. Keluar
"""
            )

        selection = read_int("Insert nomor: ")


if __name__ == "__main__":
    main()
