from data_functions import Field, Birthday, Name, Phone, Record, AddressBook
import json

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

def add_contact(args, book):
    try:
        name, phone = args
    except ValueError:
        return "You have entered insufficient data"

    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)
    return "Contact added."

def change_username_phone(args, book):
    try:
        name, phone = args
    except ValueError:
        return "You have entered insufficient data"

    record = book.find_by_name(name)
    if record:
        record.add_phone(phone)
        return f"Contact {name} changed his phone numer for {phone}"
    else:
        return "There is no such contact"

def phone_username(args, book):
    try:
        name = args[0]
    except IndexError:
        return "That contact is not on the list"

    record = book.find_by_name(name)
    if record:
        return f"{name}`s phone numer is {record.phones[0]}"
    else:
        return "There is no such contact"

def all_contacts(book):
    contact_list = ""
    for record in book.data:
        contact_list += str(record) + "\n"
    return contact_list

def add_birthday(args, book):
    try:
        name, birthday = args
    except ValueError:
        return "Insufficient data provided. Please provide both name and birthday in the format DD.MM.YYYY."

    record = book.find_by_name(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added for {name}: {birthday}"
    else:
        return f"Contact {name} not found."

def show_birthday(args, book):
    try:
        name = args[0]
    except IndexError:
        return "Please provide the name of the contact whose birthday you want to show."

    record = book.find_by_name(name)
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

    with open('test_data.json', 'r') as file:
        test_data = json.load(file)
        for contact_data in test_data['contacts']:
            record = Record(contact_data['name'], contact_data['birthday'])
            record.add_phone(contact_data['phone'])
            book.add_record(record)

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            if book.modified:
                with open('test_data.json', 'w') as file:
                    json.dump({'contacts': [record.__dict__ for record in book.data]}, file, indent=4)
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
            print(phone_username(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()