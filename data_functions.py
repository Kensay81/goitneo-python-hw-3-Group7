from collections import UserDict, defaultdict
from datetime import date, datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Birthday(Field):
    def __init__(self, birthday:str):
        try:
            datetime_object = datetime.strptime(birthday, "%d.%m.%Y")
            super().__init__(datetime_object.date())
        except ValueError:
            raise ValueError("Birthday must be in DD.MM.YYYY format")
        
    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
    

        
class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __str__(self):
        return self.value

class Phone(Field):
    def __init__(self, phone):
        if self.validate_number(phone):
            super().__init__(phone)
        else:
            raise ValueError("Invalid phone number format")

    def validate_number(self, phone):
        patterns = ["(", "-", ")", "+", " ", "."]
        clear_phone = phone.strip()
        for pattern in patterns:
            clear_phone = clear_phone.replace(pattern, "")
        return len(clear_phone) == 10 and clear_phone.isdigit()

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = None if birthday is None else Birthday(birthday)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                break

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        phones_str = ", ".join(str(phone) for phone in self.phones)
        if hasattr(self, 'birthday'):
            return f"Contact name: {self.name}, phones: {phones_str}, birthday: {self.birthday}"
        else:
            return f"Contact name: {self.name}, phones: {phones_str}"
    
    def add_birthday(self, birthday):
        if self.birthday is not None:
            raise ValueError("Birthday is already set. Use another method if you need to change it.")
        self.birthday = Birthday(birthday)


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Only Record objects can be added to AddressBook")
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data.get(name)
        else:
            raise Exception(f"{name} is not in the Address book")

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise Exception(f"{name} is not in the Address book")
        
    def get_birthdays_per_week(self):
        today = datetime.today().date()

        # Подготовка индексов по дням недели от текущего дня
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        today_index = today.weekday()
        sorted_days = days_of_week[today_index:] + days_of_week[:today_index]
        next_week_birthdays = defaultdict(list)

        # Поиск в списке всех именинников на ближайшие 7 дней, включая текущий день    
        for record in self.data.values():
            if record.birthday:
                birthday = record.birthday.value
                birthday_this_year = birthday.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                delta_days = (birthday_this_year - today).days
                if delta_days < 7:
                    next_week_birthdays[birthday_this_year.strftime("%A")].append(record.name.value)

        # Сортировка дней рождений с учетом условий задачи (перенос с выходных на понедельник,
        # сортировка от сегодняшнего дня по дням недели)   
        sorted_birthdays = {}
        for day in sorted_days:
            if day in next_week_birthdays:  
                if day == "Saturday" or day == "Sunday":
                    sorted_birthdays["Monday"] = next_week_birthdays[day]
                else:
                    sorted_birthdays[day] = next_week_birthdays[day] 

        # Вывод результатов
        if len(sorted_birthdays) == 0:
            print("No one on your list has a birthday this week.")
        else:
            for day, names in sorted_birthdays.items():
                print(f"{day}: {', '.join(names)}")    

        return sorted_birthdays


