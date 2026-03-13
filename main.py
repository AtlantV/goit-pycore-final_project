"""
Main — точка входу, CLI інтерфейс
==================================
Містить парсер команд, обробники та головний цикл.
"""

from address_book import AddressBook, Record
from storage import save_data, load_data


# ---- Декоратор для обробки помилок ----

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and(or) phone (12 numbers) please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Not enough arguments."
    return inner


# ---- Парсер команд ----

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


# ---- Обробники команд для контактів ----

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_number, new_number, *_ = args
    record = book.find(name)
    if record is None:
        return "No such name in AddressBook."
    record.edit_phone(old_number, new_number)
    return "Contact updated."


@input_error
def phone_username(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "No such name in AddressBook."
    return str(record)


def all_contacts(book: AddressBook):
    if not book:
        return "No records found."
    return "\n".join(str(record) for record in book.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return "No such name in AddressBook."
    record.add_birthday(birthday)
    return f"Birthday for {name} added."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "No such name in AddressBook."
    if record.birthday is None:
        return "No birthday set."
    return f"{name}: {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def birthdays(args, book: AddressBook):
    result = book.get_upcoming_birthdays()
    if not result:
        return "No upcoming birthdays."
    return "\n".join(f"{item['name']}: {item['congratulation_date']}" for item in result)

@input_error
def add_email(args, book: AddressBook):
    name, email, *_ = args
    record = book.find(name)
    if record is None:
        return "No such name in AddressBook."
    record.add_email (email)
    return f"Email for {name} added."

@input_error
def add_address(args, book: AddressBook):
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        return "No such name in AddressBook."
    record.add_address (address)
    return f"Address for {name} added."

@input_error
def delete (args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record is None:
        return "No such name in AddressBook."
    book.delete(name)
    return f"Record for {name} deleted."

# ---- Головний цикл ----

def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    print("Commands: add, change, phone, all, add-birthday, show-birthday, birthdays, add-email, add-address, exit/close")

    while True:
        user_input = input("-> ").strip()
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(phone_username(args, book))

        elif command == "all":
            print(all_contacts(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        elif command == "add-email":
            print(add_email(args, book))
        
        elif command == "add-address":
            print(add_address(args, book))

        elif command == "delete":
            print(delete(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()