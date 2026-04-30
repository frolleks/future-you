TIMELINE_YEARS = [1, 5, 10, 20, 30]

ascii = """ 

  ______     _                   __     __         
 |  ____|   | |                  \ \   / /         
 | |__ _   _| |_ _   _ _ __ ___   \ \_/ /__  _   _ 
 |  __| | | | __| | | | '__/ _ \   \   / _ \| | | |
 | |  | |_| | |_| |_| | | |  __/    | | (_) | |_| |
 |_|   \__,_|\__|\__,_|_|  \___|    |_|\___/ \__,_|
                                                                                                  
"""

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

    is_positive = read_yes_no("Apakah kebiasaan ini positif/menghasilkan uang? (y/n): ")

    if is_positive:
        habit_return_back = read_float(
            f"Masukkan uang yang kembali setiap {habit_interval} hari: "
        )
    else:
        habit_return_back = 0

    habits.append({
        "name": habit_name,
        "interval": habit_interval,
        "cost": habit_cost,
        "is_positive": is_positive,
        "return_back": habit_return_back
    })


def show_timeline(habits, purchases, saldo, annual_return):
    annual_rate = annual_return / 100

    for years in TIMELINE_YEARS:
        total_habit_cost = 0
        total_habit_return = 0

        for habit in habits:
            total_days = years * 365
            times_done = total_days / habit["interval"]

            total_habit_cost += habit["cost"] * times_done
            total_habit_return += habit["return_back"] * times_done

        total_product_return = 0

        for item in purchases:
            total_product_return += item["annual_return_back"] * years

        money_before_investment = (
            saldo
            - total_habit_cost
            + total_habit_return
            + total_product_return
        )

        money_after_investment = money_before_investment * ((1 + annual_rate) ** years)

        print(f"""
{years} tahun
Saldo sekarang: {format_money(saldo)}
Total biaya kebiasaan: {format_money(total_habit_cost)}
Total return kebiasaan: {format_money(total_habit_return)}
Total return produk: {format_money(total_product_return)}
Uang sebelum investasi: {format_money(money_before_investment)}
Uang setelah investasi: {format_money(money_after_investment)}
""")


def show_profile(habits):
    if len(habits) > 0:
        print("Daftar semua kebiasaan:")
        for i in range(len(habits)):
            habit = habits[i]

            print(f"""
{i + 1}. {habit["name"]}
Frekuensi: setiap {habit["interval"]} hari
Biaya setiap {habit["interval"]} hari: {format_money(habit["cost"])}
Positif: {"Ya" if habit["is_positive"] else "Tidak"}
Return setiap {habit["interval"]} hari: {format_money(habit["return_back"])}
""")
    else:
        print("Tidak ada kebiasaan untuk dilihat.")


def add_item_to_catalog(catalog):
    created = False

    while created == False:
        name = input("Masukkan nama barang baru: ")
        price = read_float("Masukkan harga barang: ")
        annual_return_back = read_float("Masukkan uang yang kembali dari barang ini per tahun: ")

        if price <= 0:
            print("Harga harus lebih dari 0.")
            continue

        new_item = {
            "name": name,
            "price": price,
            "annual_return_back": annual_return_back
        }

        catalog.append(new_item)
        created = True

    print(f"{name} berhasil ditambahkan ke katalog.")


def open_store(saldo, purchases):
    catalog = [
        {"name": "Laptop buat produktivitas", "price": 30000000, "annual_return_back": 8},
        {"name": "Kursus leher ke atas", "price": 3500000, "annual_return_back": 2},
        {"name": "Nintendo Switch 2", "price": 8000000, "annual_return_back": 0},
        {"name": "Sepatu Nike Air Jordan", "price": 1500000, "annual_return_back": 0},
    ]

    while True:
        if saldo <= 0:
            print("Anda tidak memiliki saldo.")
            break

        print(f"""
Menu Toko
Saldo: {format_money(saldo)}

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
                print(
                    f"{i + 1}. {item['name']} - "
                    f"Harga: {format_money(item['price'])} - "
                    f"Return/tahun: {format_money(item['annual_return_back'])}"
                )

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

                purchases.append({
                    "name": selected_item["name"],
                    "price": selected_item["price"],
                    "annual_return_back": selected_item["annual_return_back"]
                })

                print(f"Berhasil membeli {selected_item['name']}.")
                print(f"Sisa saldo: {format_money(saldo)}")
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
                    item = purchases[i]
                    print(
                        f"{i + 1}. {item['name']} - "
                        f"Harga: {format_money(item['price'])} - "
                        f"Return/tahun: {format_money(item['annual_return_back'])}"
                    )

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
        print(ascii)
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

            show_timeline(habits, purchases, saldo, annual_return)

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
