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


def read_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()

        if answer in ("y", "ya"):
            return True

        if answer in ("n", "no", "tidak"):
            return False

        print("Jawab dengan y/ya atau n/tidak.")


def create_investment_plan():
    initial_amount = read_float("Masukkan jumlah uang awal: ", minimum=0)
    annual_rate = read_float("Masukkan return tahunan investasi (%): ", minimum=0)

    return {
        "initial_amount": initial_amount,
        "annual_rate": annual_rate,
    }


def create_goal_item():
    item_name = input("Masukkan nama goal barang: ").strip()

    while not item_name:
        print("Nama goal barang tidak boleh kosong.")
        item_name = input("Masukkan nama goal barang: ").strip()

    price = read_float("Masukkan harga goal barang: ", minimum=0)

    return {
        "name": item_name,
        "price": price,
    }


def add_goal_item(goal_items):
    item = create_goal_item()
    existing_names = {goal["name"].lower() for goal in goal_items}

    if item["name"].lower() in existing_names:
        print("Goal barang dengan nama ini sudah ada.")
        return

    goal_items.append(item)
    print(f"Goal barang {item['name']} berhasil ditambahkan.")


def setup_goal_items():
    goal_items = []

    while read_yes_no("Tambah goal barang sekali beli sekarang? (y/n): "):
        add_goal_item(goal_items)

    return goal_items


def create_habit():
    habit_name = input("Masukkan nama kebiasaan yang ingin dikurangi: ").strip()

    while not habit_name:
        print("Nama kebiasaan tidak boleh kosong.")
        habit_name = input("Masukkan nama kebiasaan yang ingin dikurangi: ").strip()

    daily_cost = read_float("Masukkan penggunaan uang per hari: ", minimum=0)

    return {
        "name": habit_name,
        "daily_cost": daily_cost,
        "monthly_investment": daily_cost * 30,
    }


def calculate_lump_sum_growth(initial_amount, annual_rate, years):
    monthly_rate = annual_rate / 100 / 12
    months = years * 12

    return initial_amount * ((1 + monthly_rate) ** months)


def calculate_monthly_growth(monthly_investment, annual_rate, years):
    monthly_rate = annual_rate / 100 / 12
    months = years * 12

    if monthly_rate == 0:
        return monthly_investment * months

    return monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate)


def calculate_total_monthly_savings(habits):
    total = 0

    for habit in habits:
        total += habit["monthly_investment"]

    return total


def calculate_timeline(investment_plan, habits):
    results = {}
    monthly_savings = calculate_total_monthly_savings(habits)

    for years in TIMELINE_YEARS:
        initial_growth = calculate_lump_sum_growth(
            investment_plan["initial_amount"],
            investment_plan["annual_rate"],
            years,
        )
        habit_growth = calculate_monthly_growth(
            monthly_savings,
            investment_plan["annual_rate"],
            years,
        )
        total_value = initial_growth + habit_growth

        results[years] = {
            "initial_growth": initial_growth,
            "habit_growth": habit_growth,
            "total_value": total_value,
            "opportunity_gain": total_value - investment_plan["initial_amount"],
        }

    return results


def show_timeline(results):
    max_value = max(result["total_value"] for result in results.values())

    print("\nFuture You Timeline")
    print("-------------------")

    for years, result in results.items():
        value = result["total_value"]
        bar_length = int((value / max_value) * 40) if max_value > 0 else 0
        bar = "#" * bar_length
        print(f"{years:>2} years | {bar:<40} {format_money(value)}")
        print(
            f"          uang awal: {format_money(result['initial_growth'])}"
            f" | habit avoided: {format_money(result['habit_growth'])}"
            f" | opportunity gain: {format_money(result['opportunity_gain'])}"
        )


def show_buying_power(value, goal_items):
    print("\nGoal barang yang terjangkau dari timeline:")

    if not goal_items:
        print("- Belum ada goal barang yang dibuat.")
        return

    affordable_goals = 0
    for goal in goal_items:
        if value >= goal["price"]:
            print(f"- {goal['name']} ({format_money(goal['price'])})")
            affordable_goals += 1

    if affordable_goals == 0:
        print("- Belum ada goal barang yang terjangkau.")


def calculate_purchase_total(purchases):
    total = 0

    for purchase in purchases:
        total += purchase["price"]

    return total


def get_store_budget(investment_plan):
    return investment_plan["initial_amount"]


def show_purchase_summary(investment_plan, purchases):
    budget = get_store_budget(investment_plan)
    spent = calculate_purchase_total(purchases)
    remaining = budget - spent

    print("\nStore Sekali Beli")
    print("-----------------")
    print(f"Budget dari uang awal: {format_money(budget)}")
    print(f"Total belanja sekali beli: {format_money(spent)}")
    print(f"Sisa budget: {format_money(remaining)}")

    if purchases:
        print("\nBarang yang sudah dibeli:")
        for purchase in purchases:
            print(f"- {purchase['name']} ({format_money(purchase['price'])})")
    else:
        print("\nBelum ada barang yang dibeli.")


def show_store_catalog(goal_items, purchases):
    purchased_names = {purchase["name"] for purchase in purchases}

    print("\nGoal Barang")
    print("-----------")

    if not goal_items:
        print("Belum ada goal barang. Tambahkan goal dulu dari menu toko.")
        return

    for index, item in enumerate(goal_items, start=1):
        status = "sudah dibeli" if item["name"] in purchased_names else "tersedia"
        print(f"{index}. {item['name']} - {format_money(item['price'])} ({status})")


def buy_item(item, investment_plan, purchases):
    purchased_names = {purchase["name"] for purchase in purchases}

    if item["name"] in purchased_names:
        print("Barang ini sudah pernah dibeli. Pembelian hanya bisa sekali.")
        return

    budget = get_store_budget(investment_plan)
    remaining = budget - calculate_purchase_total(purchases)

    if item["price"] > remaining:
        print("Budget belum cukup untuk membeli barang ini.")
        return

    purchases.append({"name": item["name"], "price": item["price"]})
    print(f"Berhasil membeli {item['name']} seharga {format_money(item['price'])}.")
    print("Pembelian ini sekali beli dan tidak menjadi habit.")


def open_store(investment_plan, goal_items, purchases):
    while True:
        show_purchase_summary(investment_plan, purchases)
        show_store_catalog(goal_items, purchases)

        print(
            """
Menu Toko
1. Beli goal barang
2. Tambah goal barang
3. Lihat ringkasan belanja
0. Kembali ke menu utama
"""
        )

        selection = read_int("Insert nomor: ")

        if selection == 1:
            if not goal_items:
                print("Belum ada goal barang untuk dibeli.")
                continue

            item_number = read_int("Pilih nomor barang: ")
            if item_number < 1 or item_number > len(goal_items):
                print("Barang tidak tersedia.")
                continue

            buy_item(goal_items[item_number - 1], investment_plan, purchases)
        elif selection == 2:
            add_goal_item(goal_items)
        elif selection == 3:
            show_purchase_summary(investment_plan, purchases)
        elif selection == 0:
            break
        else:
            print("Pilihan tidak tersedia.")


def show_investment_summary(investment_plan):
    print("\nInvestment Plan")
    print("---------------")
    print(f"Initial money: {format_money(investment_plan['initial_amount'])}")
    print(f"Annual return: {investment_plan['annual_rate']}%")


def show_habits_summary(habits):
    print("\nHabits to Avoid")
    print("---------------")

    if not habits:
        print("Belum ada kebiasaan yang ditambahkan.")
        return

    for index, habit in enumerate(habits, start=1):
        print(
            f"{index}. {habit['name']} | daily: {format_money(habit['daily_cost'])}"
            f" | monthly saved: {format_money(habit['monthly_investment'])}"
        )

    print(f"Total monthly savings: {format_money(calculate_total_monthly_savings(habits))}")


def show_goal_items_summary(goal_items):
    print("\nGoal Barang Sekali Beli")
    print("-----------------------")

    if not goal_items:
        print("Belum ada goal barang yang dibuat.")
        return

    for index, item in enumerate(goal_items, start=1):
        print(f"{index}. {item['name']} - {format_money(item['price'])}")


def show_profile(investment_plan, habits, goal_items):
    if investment_plan is None:
        print("\nInvestment Plan belum dibuat.")
    else:
        show_investment_summary(investment_plan)

    show_habits_summary(habits)
    show_goal_items_summary(goal_items)


def run_simulation(investment_plan, habits, goal_items):
    results = calculate_timeline(investment_plan, habits)
    final_year = max(results)
    final_value = results[final_year]["total_value"]

    show_profile(investment_plan, habits, goal_items)
    show_timeline(results)
    show_buying_power(final_value, goal_items)

    return results


def main():
    investment_plan = None
    habits = []
    goal_items = []
    purchases = []

    while True:
        print(
            """
Menu Utama
1. Masukkan atau ubah uang awal
2. Tambah kebiasaan yang ingin dihindari
3. Lihat profil dan kebiasaan
4. Buka timeline opportunity cost
5. Hapus semua kebiasaan
6. Tambah goal barang sekali beli
7. Buka toko barang sekali beli
0. Keluar
"""
        )

        selection = read_int("Insert nomor: ")

        if selection == 1:
            investment_plan = create_investment_plan()
            goal_items = setup_goal_items()
            purchases = []
            show_investment_summary(investment_plan)
        elif selection == 2:
            if investment_plan is None:
                print("Masukkan uang awal dulu sebelum menambahkan kebiasaan.")
                continue

            habits.append(create_habit())
            show_habits_summary(habits)
        elif selection == 3:
            show_profile(investment_plan, habits, goal_items)
        elif selection == 4:
            if investment_plan is None:
                print("Masukkan uang awal dulu sebelum membuka timeline.")
                continue

            run_simulation(investment_plan, habits, goal_items)
        elif selection == 5:
            habits = []
            print("Semua kebiasaan sudah dihapus.")
        elif selection == 6:
            if investment_plan is None:
                print("Masukkan uang awal dulu sebelum menambahkan goal barang.")
                continue

            add_goal_item(goal_items)
            show_goal_items_summary(goal_items)
        elif selection == 7:
            if investment_plan is None:
                print("Masukkan uang awal dulu sebelum membuka toko.")
                continue

            open_store(investment_plan, goal_items, purchases)
        elif selection == 0:
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak tersedia.")


if __name__ == "__main__":
    main()
