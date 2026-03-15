"""
Storage — збереження та завантаження даних
==========================================
Відповідає за запис і читання даних з диску.
"""

import pickle
from pathlib import Path
from address_book import AddressBook
from notes import NotesBook

DATA_DIR = Path.home() / ".personal_assistant"
DATA_DIR.mkdir(exist_ok=True)

BOOK_FILE = DATA_DIR / "addressbook.pkl"
NOTES_FILE = DATA_DIR / "notesbook.pkl"

def save_data(address_book, notes_book=None):
    """Зберігає адресну книгу та нотатки у файли."""
    with open(BOOK_FILE, "wb") as f:
        pickle.dump(address_book, f)

    if notes_book is not None:
        with open(NOTES_FILE, "wb") as f:
            pickle.dump(notes_book, f)


def load_data():
    """Завантажує адресну книгу та нотатки з файлів.
    Якщо файли не знайдено — повертає нові книги."""
    try:
        with open(BOOK_FILE, "rb") as f:
            address_book = pickle.load(f)
    except FileNotFoundError:
        address_book = AddressBook()

    try:
        with open(NOTES_FILE, "rb") as f:
            notes_book = pickle.load(f)
    except FileNotFoundError:
        notes_book = NotesBook()

    return address_book, notes_book