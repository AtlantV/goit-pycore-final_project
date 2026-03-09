"""
Address Book — моделі даних
============================
Містить усі класи для роботи з контактами.
"""

from collections import UserDict
from datetime import datetime, timedelta


class Field:
    """Базовий клас для полів запису."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту. Обов'язкове поле."""
    pass


class Phone(Field):
    """Клас для зберігання номера телефону. Валідація: 10 цифр."""
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Please insert 10 numbers")
        super().__init__(value)


class Birthday(Field):
    """Клас для зберігання дня народження. Формат: DD.MM.YYYY"""
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    """Клас для зберігання інформації про контакт."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                break

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    """Клас для зберігання записів та керування ними."""

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        greet_list_of_dict = []
        today_date = datetime.today().date()

        for user in self.data.values():
            if user.birthday is None:
                continue
            birth_date = user.birthday.value.date()
            birthday_this_year = birth_date.replace(year=today_date.year)

            if birthday_this_year < today_date:
                birthday_this_year = birthday_this_year.replace(year=today_date.year + 1)

            delta_days = (birthday_this_year - today_date).days
            if 1 <= delta_days <= 7:
                if birthday_this_year.weekday() == 5:
                    birthday_this_year += timedelta(days=2)
                elif birthday_this_year.weekday() == 6:
                    birthday_this_year += timedelta(days=1)
                greet_list_of_dict.append({
                    "name": user.name.value,
                    "congratulation_date": birthday_this_year.strftime("%d-%m-%Y")
                })
        return greet_list_of_dict