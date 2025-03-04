import hashlib
import mmh3
import bitarray

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray.bitarray(size)
        self.bit_array.setall(0)
    
    def _hashes(self, item: str):
        return [mmh3.hash(item, i) % self.size for i in range(self.num_hashes)]
    
    def add(self, item: str):
        for hash_value in self._hashes(item):
            self.bit_array[hash_value] = 1
    
    def contains(self, item: str) -> bool:
        return all(self.bit_array[hash_value] for hash_value in self._hashes(item))

def check_password_uniqueness(bloom_filter: BloomFilter, passwords: list):
    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password.strip():
            results[password] = "Некоректний пароль"
        elif bloom_filter.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)
    return results

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)
    
    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)
    
    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None]
    results = check_password_uniqueness(bloom, new_passwords_to_check)
    
    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
