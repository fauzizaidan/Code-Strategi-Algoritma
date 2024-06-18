import itertools
import time

# Fungsi untuk menerima input dari pengguna
def get_input():
    tasks = []
    num_tasks = int(input("Masukkan jumlah tugas: "))
    for i in range(num_tasks):
        name = input(f"Masukkan nama tugas ke-{i + 1}: ")
        duration = int(input(f"Masukkan durasi tugas {name} (dalam menit): "))
        relaxation_time = int(input(f"Masukkan waktu santai untuk tugas {name} (dalam menit): "))
        tasks.append((name, duration, relaxation_time))
    max_hours = int(input("Masukkan waktu maksimal yang tersedia per hari (dalam jam): "))
    max_time = max_hours * 60  # Konversi ke menit
    return tasks, max_time

# Fungsi brute force
def brute_force(tasks, max_time):
    start = time.perf_counter()
    
    all_combinations = list(itertools.chain.from_iterable(itertools.combinations(tasks, r) for r in range(1, len(tasks) + 1)))
    optimal_value = 0
    optimal_combination = []
    
    for comb in all_combinations:
        total_duration = sum(task[1] for task in comb)
        total_value = sum(task[2] for task in comb)
        
        if total_duration <= max_time and total_value > optimal_value:
            optimal_value = total_value
            optimal_combination = comb

    total_duration = sum(task[1] for task in optimal_combination)
    
    end = time.perf_counter()
    exec_time = (end - start) * 1000

    return optimal_combination, optimal_value, exec_time, total_duration

# Fungsi greedy berdasarkan waktu santai terbesar
def greedy_by_relaxation_time(tasks, max_time):
    start = time.perf_counter()

    sorted_tasks = sorted(tasks, key=lambda x: x[2], reverse=True)
    total_duration = 0
    total_value = 0
    selected_tasks = []

    for task in sorted_tasks:
        if total_duration + task[1] <= max_time:
            selected_tasks.append(task)
            total_duration += task[1]
            total_value += task[2]

    end = time.perf_counter()
    exec_time = (end - start) * 1000

    return selected_tasks, total_value, exec_time, total_duration

# Fungsi greedy berdasarkan durasi terpendek
def greedy_by_duration(tasks, max_time):
    start = time.perf_counter()

    sorted_tasks = sorted(tasks, key=lambda x: x[1])
    total_duration = 0
    total_value = 0
    selected_tasks = []

    for task in sorted_tasks:
        if total_duration + task[1] <= max_time:
            selected_tasks.append(task)
            total_duration += task[1]
            total_value += task[2]

    end = time.perf_counter()
    exec_time = (end - start) * 1000

    return selected_tasks, total_value, exec_time, total_duration

# Fungsi greedy berdasarkan rasio waktu santai per durasi (density) terbesar
def greedy_by_density(tasks, max_time):
    start = time.perf_counter()

    sorted_tasks = sorted(tasks, key=lambda x: x[2] / x[1], reverse=True)
    total_duration = 0
    total_value = 0
    selected_tasks = []

    for task in sorted_tasks:
        if total_duration + task[1] <= max_time:
            selected_tasks.append(task)
            total_duration += task[1]
            total_value += task[2]

    end = time.perf_counter()
    exec_time = (end - start) * 1000

    return selected_tasks, total_value, exec_time, total_duration

# Fungsi untuk mencetak hasil
def print_results(method, selected_tasks, total_value, exec_time, total_duration):
    print(f"\n{method}:")
    print("Tugas yang Dipilih:")
    for task in selected_tasks:
        print(f"  {task[0]}: Durasi {task[1]} menit, Waktu Santai {task[2]} menit")
    print(f"Total Durasi Tugas: {total_duration} menit")
    print(f"Total Waktu Santai: {total_value} menit")
    print(f"Waktu Eksekusi: {exec_time:.2f} milidetik")

if __name__ == "__main__":
    tasks, max_time = get_input()

    # Brute Force
    selected_tasks_brute, total_value_brute, exec_time_brute, total_duration_brute = brute_force(tasks, max_time)
    print_results("Brute Force", selected_tasks_brute, total_value_brute, exec_time_brute, total_duration_brute)

    # Memilih strategi greedy terbaik berdasarkan hasil eksekusi
    greedy_strategies = {
        "Greedy by Relaxation Time": greedy_by_relaxation_time,
        "Greedy by Duration": greedy_by_duration,
        "Greedy by Density": greedy_by_density
    }
    
    best_greedy_result = None
    best_greedy_method = None

    for method, func in greedy_strategies.items():
        selected_tasks_greedy, total_value_greedy, exec_time_greedy, total_duration_greedy = func(tasks, max_time)
        if best_greedy_result is None or total_value_greedy > best_greedy_result[1]:
            best_greedy_result = (selected_tasks_greedy, total_value_greedy, exec_time_greedy, total_duration_greedy)
            best_greedy_method = method
    
    print_results(best_greedy_method, *best_greedy_result)
