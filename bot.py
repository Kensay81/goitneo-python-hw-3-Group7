from data_functions import Field, Birthday, Name, Phone, Record, AddressBook

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def add_contact(args, contacts):
    try:
        name, phone = args
    except:
        return "You have entered insufficient data"
    if name not in contacts:
        contacts[name] = phone
    else:
        return "This contact already exists"
    return "Contact added."

def change_username_phone(args, contacts):
    try:
        name, phone = args
    except:
        return "You have entered insufficient data"
    if name in contacts:
        contacts[name] = phone
    else:
        return "There is no such contact"
    return f"Contact {name} changed his phone numer for {phone}"

def phone_username(args, contacts):
    try:
        name = args[1]
    except:
        return "That contact is not on the list"
    if name in contacts:
        phone = contacts[name]
    else:
        return "There is no such contact"
    return f"{name}`s phone numer is {phone}"

def all_contacts(args, contacts):
    phonebook = ""
    for name, phone in contacts.items():
        phonebook += f"{name}: {phone} \n"
    return phonebook

def add_birthday(args, book):
    try:
        name, birthday = args
    except ValueError:
        return "Insufficient data provided. Please provide both name and birthday in the format DD.MM.YYYY."

    try:
        record = book.find(name)
        if record:
            record.add_birthday(birthday)
            return f"Birthday added for {name}: {birthday}"
        else:
            return f"Contact {name} not found."
    except Exception as e:
        return str(e)


def show_birthday(args, book):
    try:
        name = args[0]
    except IndexError:
        return "Please provide the name of the contact whose birthday you want to show."

    try:
        record = book.find(name)
        if record:
            if record.birthday:
                return f"{name}'s birthday: {record.birthday}"
            else:
                return f"{name} does not have a birthday set."
        else:
            return f"Contact {name} not found."
    except Exception as e:
        return str(e)

def birthdays(book):
    return book.get_birthdays_per_week()



def main():
    #contacts = {"Ilya": "015140749275", "Olya":"015172836348", "Denis":"017673560531" }
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
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            with open('test_data.json', 'w') as file:
                json.dump({'contacts': [record.__dict__ for record in book.data.values()]}, file, indent=4)
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "all":
            print(all_contacts(args, book))
        elif command == "change":
            print(change_username_phone(args, book))
        elif command == "phone" and "username" in user_input: 
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

