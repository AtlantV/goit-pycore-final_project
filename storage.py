"""
Storage — збереження та завантаження даних
==========================================
Відповідає за запис і читання даних з диску.
"""

import pickle
from address_book import AddressBook
from notes import NotesBook


def save_data(address_book, notes_book=None, address_file="addressbook.pkl", notes_file="notesbook.pkl"):
    """Зберігає адресну книгу та нотатки у файли."""
    with open(address_file, "wb") as f:
        pickle.dump(address_book, f)
    
    if notes_book is not None:
        with open(notes_file, "wb") as f:
            pickle.dump(notes_book, f)


def load_data(address_file="addressbook.pkl", notes_file="notesbook.pkl"):
    """Завантажує адресну книгу та нотатки з файлів.
    Якщо файли не знайдено — повертає нові книги."""
    try:
        with open(address_file, "rb") as f:
            address_book = pickle.load(f)
    except FileNotFoundError:
        address_book = AddressBook()
    
    try:
        with open(notes_file, "rb") as f:
            notes_book = pickle.load(f)
    except FileNotFoundError:
        notes_book = NotesBook()
    
    return address_book, notes_book