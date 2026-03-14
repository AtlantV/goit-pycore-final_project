"""
Address Book — моделі даних
============================
Містить усі класи для роботи з контактами.
"""

from collections import UserDict
from datetime import datetime, timedelta
import re

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
    """Клас для зберігання номера телефону. Валідація: 12 цифр."""
    def __init__(self, value):
        if not re.match(r"^380\d{9}$", value):
            raise ValueError("Please insert 12 numbers in format '380*' :")
        super().__init__(value)

class Birthday(Field):
    """Клас для зберігання дня народження. Формат: DD.MM.YYYY"""
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Email(Field):
    """Клас для зберігання email. Формат: *@*.*"""
    def __init__(self, value):
        if not re.match(r"^[\w.-]+@[\w.-]+\.\w{2,}$", value):  
          raise ValueError("Invalid email")
        super().__init__(value)

class Address(Field):
    """Клас для зберігання address. Формат: місто, вулиця, будинок, квартира (якщо є)"""
    def __init__(self, value):
        # Очікуємо рядок у форматі: "місто, вулиця, будинок, квартира (якщо є)"
        parts = [p.strip() for p in value.split(",")]
        
        if len(parts) < 3: 
            raise ValueError("Address must contain at least city, street and house number")

        city, street, house = parts[0], parts[1], parts[2]
        apartment = parts[3] if len(parts) == 4 else None

        # Валідація: місто і вулиця — тільки букви та пробіли
        if not re.match(r"^[А-ЯІЇЄҐа-яієїґA-Za-z\s-]+$", city):
            raise ValueError("Invalid city name")
        if not re.match(r"^[А-ЯІЇЄҐа-яієїґA-Za-z\s-]+$", street):
            raise ValueError("Invalid street name")
        if not re.match(r"^\d+[\w/\-]*$", house):
            raise ValueError("Invalid house number")
        if apartment and not apartment.isdigit():
            raise ValueError("Apartment number must be digits")

        # Форматування у стандартний вигляд
        formatted = f"м. {city}, вул. {street}, буд. {house}"
        if apartment:
            formatted += f", кв. {apartment}"
        super().__init__(formatted)


class Record:
    """Клас для зберігання інформації про контакт."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.email = None 
        self.address = None

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

    def add_email(self, email):
        self.email = Email(email)
    
    def add_address(self, address):
        self.address = Address(address)

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime('%d.%m.%Y') if self.birthday else "N/A"
        email = self.email.value if self.email else "N/A"
        address = self.address.value if self.address else "N/A"

        return (
        f"Contact name: {self.name.value}, "
        f"phones: {phones}, "
        f"birthday: {birthday}, "
        f"email: {email}, "
        f"address: {address}"
    )

class AddressBook(UserDict):
    """Клас для зберігання записів та керування ними."""

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days):
        upcoming_birthdays = []
        today = datetime.today().date()
        end_date = today + timedelta(days=days)

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value.date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            if today <= birthday_this_year <= end_date:
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": birthday_this_year.strftime("%d.%m.%Y")
                })

        return upcoming_birthdays