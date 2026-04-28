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


def create_habit():
    habit_name = input("Masukkan nama kebiasaan yang ingin dikurangi: ").strip()

    while not habit_name:
        print("Nama kebiasaan tidak boleh kosong.")
        habit_name = input("Masukkan nama kebiasaan yang ingin dikurangi: ").strip()

    daily_cost = read_float("Masukkan penggunaan uang per hari: ", minimum=0)
    annual_rate = read_float("Masukkan return tahunan investasi (%): ", minimum=0)

    return {
        "name": habit_name,
        "daily_cost": daily_cost,
        "annual_rate": annual_rate,
        "monthly_investment": daily_cost * 30,
    }


def calculate_future_value(monthly_investment, annual_rate, years):
    monthly_rate = annual_rate / 100 / 12
    months = years * 12

    if monthly_rate == 0:
        return monthly_investment * months

    return monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate)


def calculate_timeline(habit):
    results = {}

    for years in TIMELINE_YEARS:
        results[years] = calculate_future_value(
            habit["monthly_investment"],
            habit["annual_rate"],
            years,
        )

    return results


def show_timeline(results):
    max_value = max(results.values())

    print("\nFuture You Timeline")
    print("-------------------")

    for years, value in results.items():
        bar_length = int((value / max_value) * 40) if max_value > 0 else 0
        bar = "#" * bar_length
        print(f"{years:>2} years | {bar:<40} {format_money(value)}")


def show_buying_power(value):
    goals = {
        "local trip": 10000000,
        "international trip": 300000000,
        "used car": 100000000,
        "house down payment": 500000000,
    }

    print("\nYang Anda bisa beli:")

    affordable_goals = 0
    for goal, price in goals.items():
        if value >= price:
            print(f"- {goal} ({format_money(price)})")
            affordable_goals += 1

    if affordable_goals == 0:
        print("- Keep going. Your future balance is still building.")


def show_habit_summary(habit):
    print("\nHabit Summary")
    print("-------------")
    print(f"Habit: {habit['name']}")
    print(f"Daily cost: {format_money(habit['daily_cost'])}")
    print(f"Monthly investment: {format_money(habit['monthly_investment'])}")
    print(f"Annual return: {habit['annual_rate']}%")


def run_simulation(habit):
    results = calculate_timeline(habit)
    final_year = max(results)
    final_value = results[final_year]

    show_habit_summary(habit)
    show_timeline(results)
    show_buying_power(final_value)

    return results


def main():
    habit = None
    timeline_results = None

    while True:
        print(
            """
Menu Utama
1. Buat atau ubah kebiasaan
2. Jalankan simulasi compound interest
3. Buka timeline terakhir
0. Keluar
"""
        )

        try:
            selection = int(input("Insert nomor: "))
        except ValueError:
            print("Input bukanlah nomor!")
            continue

        if selection == 1:
            habit = create_habit()
            timeline_results = None
            show_habit_summary(habit)
        elif selection == 2:
            if habit is None:
                print("Buat kebiasaan dulu sebelum menjalankan simulasi.")
                continue

            timeline_results = run_simulation(habit)
        elif selection == 3:
            if timeline_results is None:
                if habit is None:
                    print("Buat kebiasaan dulu sebelum membuka timeline.")
                    continue

                timeline_results = calculate_timeline(habit)

            show_timeline(timeline_results)
        elif selection == 0:
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak tersedia.")


if __name__ == "__main__":
    main()
