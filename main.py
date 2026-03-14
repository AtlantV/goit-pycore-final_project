"""
Main — точка входу, CLI інтерфейс
==================================
Містить парсер команд, обробники та головний цикл.
"""

from address_book import AddressBook, Record
from notes import NotesBook, Note
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
    line = "─" * 35
    return f"\n{line}\n" + f"\n{line}\n".join(str(record) for record in book.values())

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
    days = int(args[0])

    if days < 0:
        return "Number of days must be a positive integer."

    result = book.get_upcoming_birthdays(days)

    if not result:
        return f"No birthdays in the next {days} days."

    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}" for item in result
    )

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


# ---- Обробники команд для нотаток ----

@input_error
def add_note(args, notes_book: NotesBook):
    """Додає нотатку. Використання: add-note <назва> | <текст>"""
    if "|" not in " ".join(args):
        return "Use format: add-note <title> | <text>"
    
    full_input = " ".join(args)
    parts = full_input.split("|", 1)
    title = parts[0].strip()
    text = parts[1].strip()
    
    if not title or not text:
        return "Title and text cannot be empty."
    
    note = Note(title, text)
    notes_book.add_note(note)
    return f"Note '{title}' added with ID: {note.id}"


@input_error
def edit_note(args, notes_book: NotesBook):
    """Редагує нотатку. Використання: edit-note <id> | <новий_текст> або edit-note <id> -title <нова_назва>"""
    if not args:
        return "Specify note ID."
    
    note_id = int(args[0])
    note = notes_book.find(note_id)
    
    if note is None:
        return f"Note with ID {note_id} not found."
    
    remaining_args = args[1:]
    
    # Редагування за опцією -title
    if remaining_args and remaining_args[0] == "-title":
        if len(remaining_args) < 2:
            return "Specify new title after -title."
        new_title = " ".join(remaining_args[1:])
        note.edit(title=new_title)
        return f"Note title updated: {new_title}"
    
    # Редагування за опцією -text або прямо з |
    full_input = " ".join(remaining_args)
    if "|" in full_input:
        parts = full_input.split("|", 1)
        new_text = parts[1].strip()
        note.edit(text=new_text)
        return f"Note with ID {note_id} updated."
    else:
        return "Use format: edit-note <id> | <new_text> or edit-note <id> -title <new_title>"


@input_error
def delete_note(args, notes_book: NotesBook):
    """Видаляє нотатку."""
    if not args:
        return "Specify note ID."
    
    note_id = int(args[0])
    if notes_book.delete(note_id):
        return f"Note with ID {note_id} deleted."
    return f"Note with ID {note_id} not found."


@input_error
def search_notes(args, notes_book: NotesBook):
    """Шукає нотатки за текстом."""
    if not args:
        return "Specify search query."
    
    query = " ".join(args)
    results = notes_book.search_by_text(query)
    
    if not results:
        return f"No notes found for query '{query}'."
    
    return "\n" + "-" * 50 + "\n" + "\n".join("-" * 50 + "\n" + str(note) for note in results)


@input_error
def search_notes_by_tag(args, notes_book: NotesBook):
    """Шукає нотатки за тегом."""
    if not args:
        return "Specify tag."
    
    tag = " ".join(args)
    results = notes_book.search_by_tag(tag)
    
    if not results:
        return f"No notes found with tag '{tag}'."
    
    return "\n" + "-" * 50 + "\n" + "\n".join("-" * 50 + "\n" + str(note) for note in results)


@input_error
def add_tag_to_note(args, notes_book: NotesBook):
    """Додає тег до нотатки."""
    if len(args) < 2:
        return "Usage: add-tag <note_id> <tag_name>"
    
    note_id = int(args[0])
    tag = " ".join(args[1:])
    
    note = notes_book.find(note_id)
    if note is None:
        return f"Note with ID {note_id} not found."
    
    note.add_tag(tag)
    return f"Tag '{tag}' added to note {note_id}."


@input_error
def remove_tag_from_note(args, notes_book: NotesBook):
    """Видаляє тег з нотатки."""
    if len(args) < 2:
        return "Usage: remove-tag <note_id> <tag_name>"
    
    note_id = int(args[0])
    tag = " ".join(args[1:])
    
    note = notes_book.find(note_id)
    if note is None:
        return f"Note with ID {note_id} not found."
    
    note.remove_tag(tag)
    return f"Tag '{tag}' removed from note {note_id}."


def all_notes(notes_book: NotesBook):
    """Виводить всі нотатки."""
    if not notes_book:
        return "No notes found."
    
    return "\n" + "-" * 50 + "\n" + "\n".join(
        "-" * 50 + "\n" + str(note) for note in notes_book.get_notes_sorted_by_date(reverse=True)
    )


def all_tags(notes_book: NotesBook):
    """Виводить всі теги."""
    tags = notes_book.get_all_tags()
    if not tags:
        return "No tags found."
    return "Available tags: " + ", ".join(tags)



def main():
    book, notes_book = load_data()
    print("=" * 70)
    print("🤖 Welcome to Personal Assistant CLI!")
    print("=" * 70)
    print("\n📒 CONTACTS: add, change, phone, all, add-birthday, show-birthday,")
    print("            birthdays, add-email, add-address, delete")
    print("\n📝 NOTES:    add-note, edit-note, delete-note, search-note,")
    print("            search-tag, add-tag, remove-tag, all-notes, all-tags")
    print("\n🔧 OTHER:    help, hello, exit/close")
    print("=" * 70 + "\n")

    while True:
        try:
            user_input = input("-> ").strip()
            if not user_input:
                continue

            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                save_data(book, notes_book)
                print("\n✅ Data saved. Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")

            elif command == "help":
                print("\n" + "=" * 70)
                print("📒 CONTACT COMMANDS:")
                print("=" * 70)
                print("  add <name> <phone>               - Add contact")
                print("  change <name> <old> <new>        - Change phone")
                print("  phone <name>                     - Show contact info")
                print("  all                              - Show all contacts")
                print("  add-birthday <name> <DD.MM.YYYY> - Add birthday")
                print("  show-birthday <name>             - Show birthday")
                print("  birthdays <days>                 - Show upcoming birthdays")
                print("  add-email <name> <email>         - Add email")
                print("  add-address <name> <address>     - Add address")
                print("  delete <name>                    - Delete contact")
                print("\n" + "=" * 70)
                print("📝 NOTE COMMANDS:")
                print("=" * 70)
                print("  add-note <title> | <text>       - Add note")
                print("  edit-note <ID> | <text>         - Edit note text")
                print("  edit-note <ID> -title <title>   - Edit note title")
                print("  delete-note <ID>                - Delete note")
                print("  search-note <query>             - Search notes by text")
                print("  search-tag <tag>                - Search notes by tag")
                print("  add-tag <ID> <tag>              - Add tag to note")
                print("  remove-tag <ID> <tag>           - Remove tag from note")
                print("  all-notes                       - Show all notes")
                print("  all-tags                        - Show all tags")
                print("\n" + "=" * 70 + "\n")

            # ---- Contact Commands ----
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
                if args:
                    print(birthdays(args, book))
                else:
                    days = input("Enter number of days: ").strip()
                    if days.isdigit():
                        print(birthdays([days], book))
                    else:
                        print("Please enter a valid number.")

            elif command == "add-email":
                print(add_email(args, book))
            
            elif command == "add-address":
                print(add_address(args, book))

            elif command == "delete":
                print(delete(args, book))

            # ---- Notes Commands ----
            elif command == "add-note":
                print(add_note(args, notes_book))

            elif command == "edit-note":
                print(edit_note(args, notes_book))

            elif command == "delete-note":
                print(delete_note(args, notes_book))

            elif command == "search-note":
                print(search_notes(args, notes_book))

            elif command == "search-tag":
                print(search_notes_by_tag(args, notes_book))

            elif command == "add-tag":
                print(add_tag_to_note(args, notes_book))

            elif command == "remove-tag":
                print(remove_tag_from_note(args, notes_book))

            elif command == "all-notes":
                print(all_notes(notes_book))

            elif command == "all-tags":
                print(all_tags(notes_book))

            else:
                print("❌ Invalid command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\n✅ Data saved. Good bye!")
            save_data(book, notes_book)
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            continue



if __name__ == "__main__":
    main()