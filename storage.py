"""
Storage — збереження та завантаження даних
==========================================
Відповідає за запис і читання даних з диску.
"""

import pickle
from address_book import AddressBook


def save_data(book, filename="addressbook.pkl"):
    """Зберігає адресну книгу у файл."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """Завантажує адресну книгу з файлу. Якщо файл не знайдено — повертає нову книгу."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()