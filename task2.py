import time
import re
from hyperloglog import HyperLogLog
import pandas as pd

def load_ips_from_log(file_path: str):
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    ip_addresses = []
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            match = ip_pattern.search(line)
            if match:
                ip_addresses.append(match.group())
    
    return ip_addresses

def count_unique_ips_set(ip_list: list) -> int:
    return len(set(ip_list))

def count_unique_ips_hyperloglog(ip_list: list, precision: float = 0.01) -> int:
    hll = HyperLogLog(precision)
    for ip in ip_list:
        hll.add(ip)
    return int(len(hll))

if __name__ == "__main__":
    log_file = "lms-stage-access.log"  # Замініть на шлях до вашого файлу
    
    # Завантаження IP-адрес
    ips = load_ips_from_log(log_file)
    print(f"Завантажено {len(ips)} IP-адрес")
    
    # Точний підрахунок унікальних IP
    start_time = time.time()
    exact_count = count_unique_ips_set(ips)
    exact_time = time.time() - start_time
    
    # Підрахунок HyperLogLog
    start_time = time.time()
    hll_count = count_unique_ips_hyperloglog(ips)
    hll_time = time.time() - start_time
    
    # Результати у вигляді таблиці
    data = {
        "Метод": ["Точний підрахунок", "HyperLogLog"],
        "Унікальні елементи": [exact_count, hll_count],
        "Час виконання (сек.)": [exact_time, hll_time]
    }
    df = pd.DataFrame(data)
    
    print(df.to_string(index=False))
