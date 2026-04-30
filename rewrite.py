TIMELINE_YEARS = [1, 5, 10, 20, 30]


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


def read_str(prompt):
    while True:
        try:
            return str(input(prompt))
        except ValueError:
            print("Input bukanlah string!")


def read_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("y", "ya"):
            return True

        if answer in ("n", "no", "tidak"):
            return False

        print("Jawab dengan y/ya atau n/tidak.")


def create_new_habit(habits):
    habit_name = read_str("Masukkan nama kebiasaan: ")
    habit_interval = read_int("Masukkan frekuensi kebiasaan ini (dalam waktu hari): ")
    habit_cost = read_float("Masukkan biaya: ")

    habits.append({"name": habit_name, "interval": habit_interval, "cost": habit_cost})


def show_timeline(habits, saldo, annual_return):
    for years in TIMELINE_YEARS:
        print(
            f"{years} tahun: {format_money(saldo + saldo * (annual_return * 100) * years)}"
        )


def show_profile(habits):
    if len(habits) > 0:
        print("Daftar semua kebiasaan:")
        for i in range(len(habits)):
            print(f"""
{i+1}. {habits[i]["name"]}
Frekuensi: setiap {habits[i]["interval"]} hari
Harga setiap {habits[i]["interval"]} hari: {format_money(habits[i]["cost"])}
    """)
    else:
        print("Tidak ada kebiasaan untuk dilihat.")


def add_item_to_catalog(catalog):
    created = False
    while created == False:
        name = input("Masukkan nama barang baru: ")
        price = read_int("Masukkan harga barang: ")

        if price <= 0:
            print("Harga harus lebih dari 0.")
            continue

        new_item = {"name": name, "price": price}

        catalog.append(new_item)
        created = True

    print(f"{name} berhasil ditambahkan ke katalog.")


def open_store(saldo, purchases):
    catalog = [
        {"name": "Pensil", "price": 3000},
        {"name": "Buku", "price": 10000},
        {"name": "Penghapus", "price": 2000},
        {"name": "Pulpen", "price": 5000},
    ]

    while True:
        if saldo <= 0:
            print("Anda tidak memiliki saldo.")
            break

        print(f"""
Menu Toko
Saldo: Rp{saldo}

1. Beli barang dari katalog
2. Tambah barang sendiri
3. Lihat daftar pembelian
0. Keluar
""")

        selection = read_int("Insert nomor: ")

        if selection == 1:
            print("\nKatalog Barang:")

            for i in range(len(catalog)):
                item = catalog[i]
                print(f"{i + 1}. {item['name']} - Rp{item['price']}")

            print("0. Batal")

            item_choice = read_int("Pilih barang: ")

            if item_choice == 0:
                continue

            if item_choice < 1 or item_choice > len(catalog):
                print("Barang tidak tersedia.")
                continue

            selected_item = catalog[item_choice - 1]

            if saldo >= selected_item["price"]:
                saldo -= selected_item["price"]
                purchases.append(selected_item["name"])

                print(f"Berhasil membeli {selected_item['name']}.")
                print(f"Sisa saldo: Rp{saldo}")
            else:
                print("Saldo tidak cukup.")

        elif selection == 2:
            add_item_to_catalog(catalog)
        elif selection == 3:
            if len(purchases) == 0:
                print("Belum ada pembelian.")
            else:
                print("\nDaftar Pembelian:")
                for i in range(len(purchases)):
                    print(f"{i + 1}. {purchases[i]}")

        elif selection == 0:
            break

        else:
            print("Tidak tersedia.")

    return saldo


def main():
    saldo = 0
    annual_return = 0
    habits = []
    purchases = []

    while True:
        if saldo > 0:
            print("""
Menu Utama
1. Masukkan atau ubah uang awal
2. Tambah investment plan
3. Tambah kebiasaan
4. Lihat profil dan kebiasaan
5. Buka timeline opportunity cost
6. Hapus semua kebiasaan
7. Buka toko barang sekali beli
0. Keluar
""")
        else:
            print("""
Menu Utama
1. Masukkan atau ubah uang awal
0. Keluar
""")

        selection = read_int("Insert nomor: ")

        if selection == 1:
            saldo = read_float("Tambah saldo ke rekening: ")
        elif selection == 2:
            if saldo == 0:
                print("Masukkan uang awal dulu.")
                continue

            annual_return = read_float("Masukkan return tahunan investasi (%): ")
        elif selection == 3:
            if saldo == 0:
                print("Masukkan uang awal dulu.")
                continue

            create_new_habit(habits)
        elif selection == 4:
            show_profile(habits)

            read_str("Pencet tombol enter untuk kembali ke menu awal: ")
        elif selection == 5:
            if saldo == 0:
                print("Masukkan uang awal dulu.")
                continue

            show_timeline(habits, saldo, annual_return)

            read_str("Pencet tombol enter untuk kembali ke menu awal: ")
        elif selection == 6:
            if len(habits) > 0:
                habits.clear()
                print("Semua kebiasaan telah dihapus.")
            else:
                print("Tidak ada kebiasaan.")
        elif selection == 7:
            saldo = open_store(saldo, purchases)
        elif selection == 0:
            break
        else:
            print("Tidak tersedia.")


if __name__ == "__main__":
    main()
