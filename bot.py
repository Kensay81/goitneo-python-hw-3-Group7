from data_functions import Field, Birthday, Name, Phone, Record, AddressBook

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def add_contact(args, book):
    try:
        name, phone = args
    except ValueError:
        return "Insufficient data provided. Please provide both name and phone number."

    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."

def change_username_phone(args, book):
    try:
        name, phone = args
    except ValueError:
        return "Insufficient data provided. Please provide both name and phone number."

    record = book.find(name)
    if record:
        record.phones = [Phone(phone)]
        return f"Contact {name} changed his phone number to {phone}"
    else:
        return f"Contact {name} not found."

def phone_username(args, book):
    try:
        name = args[0]
    except IndexError:
        return "Invalid command. Please provide a contact name."

    try:
        record = book.find(name)
        if record:
            phones = ", ".join(str(phone) for phone in record.phones) 
            return f"Contact name: {name}, phones: {phones}"
        else:
            return f"Contact {name} not found."
    except Exception as e:
        return str(e)

def all_contacts(book):
    contact_list = ""
    for record in book.data.values():
        contact_list += str(record) + "\n"
    return contact_list

def add_birthday(args, book):
    try:
        name, birthday = args
    except ValueError:
        return "Insufficient data provided. Please provide both name and birthday in the format DD.MM.YYYY."

    record = book.find(name)
    if record:
        if record.birthday:
            return f"Contact {name} already has a birthday ({record.birthday})."
        else:
            record.add_birthday(birthday)
            return f"Birthday added for {name}: {birthday}"
    else:
        return f"Contact {name} not found."


def show_birthday(args, book):
    try:
        name = args[0]
    except IndexError:
        return "Please provide the name of the contact."

    record = book.find(name)
    if record:
        if record.birthday:
            return f"{name}'s birthday: {record.birthday}"
        else:
            return f"{name} does not have a birthday set."
    else:
        return f"Contact {name} not found."

def birthdays(book):
    return book.get_birthdays_per_week()

def main():
    book = AddressBook()

    # Test data
    test_data = [
        {"name": "John", "phone": "1234567890", "birthday": "01.01.1980"},
        {"name": "Alice", "phone": "9876543210", "birthday": "02.02.1990"},
        {"name": "Bob", "phone": "5555555555", "birthday": "12.03.2000"},
        {"name": "Billy", "phone": "3805012345", "birthday": "04.04.2010"}
    ]

    # Populate the address book with test data
    for contact_data in test_data:
        record = Record(contact_data['name'], contact_data['birthday'])
        record.add_phone(contact_data['phone'])
        book.add_record(record)

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "all":
            print(all_contacts(book))
        elif command == "change":
            print(change_username_phone(args, book))
        elif command == "phone":
            if args:
                print(phone_username(args, book))
            else:
                print("Invalid command. Please provide a contact name.")
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(book.get_birthdays_per_week())
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
