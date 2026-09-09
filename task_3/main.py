from enum import Enum,auto
from abc import ABC, abstractmethod


class ItemStatus(Enum):
    AVAILABLE = auto()
    CHECKED_OUT = auto()
    LOST = auto()

class LibraryItem(ABC):

    _classes = {}

    def __init__(self, title, status = ItemStatus.AVAILABLE):
        self.title = title
        self.__status = status

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._classes[cls.__name__] = cls

    @abstractmethod
    def item_type(self):
        ...

    @property
    def item_status(self):
        return self.__status

    @staticmethod
    def isbn_check(string:str) -> bool:
        """
        Function to check the validation of ISBN-13 only
        """
        digits = string.strip().replace("-", "")

        if len(digits) != 13 or not digits.isdigit():
            return False
        
        total_sum = 0
        start = 1
        for char in digits:
            digit = int(char)
            if(start):
                total_sum += digit * 1
                start = 0
            else:
                total_sum += digit * 3
                start = 1
        return True if total_sum % 10 == 0 else False


    @classmethod
    def from_dict(cls, parsed_dict: dict):
        item_class = cls._classes[parsed_dict["type"]]
        new_dict = parsed_dict.copy()

        new_dict.pop("type")
        new_dict["status"] = ItemStatus[new_dict["status"].upper()]

        return item_class(**new_dict)

    
    def checkout(self):
        if(self.__status == ItemStatus.AVAILABLE):
            self.__status = ItemStatus.CHECKED_OUT
        else:
            raise ValueError(f"Can't Checkout {self.title} as it's {self.__status}")
    
    def return_item(self):
        if(self.__status == ItemStatus.CHECKED_OUT):
            self.__status = ItemStatus.AVAILABLE
        else:
            raise ValueError(f"Can't return_item {self.title} as it's {self.__status}")
    
    def mark_lost(self):
        if self.__status == ItemStatus.LOST:
            raise ValueError(f"Can't mark_lost {self.title} as it's {self.__status}")
        else:
            self.__status = ItemStatus.LOST

    def __lt__(self, other):
        return self.title < other.title
    
    def __str__(self):
        return f"{self.title} ({self.item_type()}) - {self.item_status.name.capitalize()}"
    
    def __repr__(self):
        return f"{self.item_type()} (title = {self.title},  {self.item_status})"

        

class Book(LibraryItem):
    loan_period = 21
    def __init__(self, title, status=ItemStatus.AVAILABLE, author=None, isbn=None, **kwargs):
        super().__init__(title, status)
        self.author = author
        self.isbn = isbn

    def item_type(self):
        return "Book"
       

class DVD(LibraryItem):
    loan_period = 5
    def __init__(self, title, status=ItemStatus.AVAILABLE, director=None,  **kwargs):
        super().__init__(title, status)
        self.director = director

    def item_type(self):
        return "DVD"
    
class Magazine(LibraryItem):
    loan_period = 14
    def __init__(self, title, status=ItemStatus.AVAILABLE, issue=None,  **kwargs):
        super().__init__(title, status)
        self.issue = issue

    def item_type(self):
        return "Magazine"

class Database:

    def loading_data(self, path) -> list[dict]:
        all_data = []

        with open(path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                data = {}
                new_line = line.rstrip().split("|")
                for sec in new_line:
                    new_sec = sec.split("=")
                    data[new_sec[0]] = new_sec[1]
                all_data.append(data)

        return all_data

    def saving_data(self, path:str, items:list[LibraryItem]):
        with open(path, 'w') as file:
            for item in items:
                line = ""
                line += f"type={item.item_type()}"
                attr = item.__dict__
                for key, value in attr.items():
                    if key == "_LibraryItem__status":
                        line += f"|status={item.item_status.name}"
                    elif value is None:
                        continue
                    else:
                        line += f"|{key}={value}"
                file.write(f"{line}\n")

            

class Library():
    def __init__(self, database:Database):
        self._items = {}
        self._database = database

    def add_item(self, item:LibraryItem):
        self._items[item.title] = item

    def checkout(self, title:str):
        self._items[title].checkout()

    def return_item(self, title):
        self._items[title].return_item()

    def find_by_title(self, title):
        if title in self._items:
            return self._items[title]
        else:
            raise ValueError(f"No such item of title {title}")
    def list_available(self) -> list[LibraryItem]:
        items = []
        for item in self._items.values():
            if item.item_status == ItemStatus.AVAILABLE:
                items.append(item)
        return items

    def load(self, path):
        data = self._database.loading_data(path)
        for item_dict in data:
            item = LibraryItem.from_dict(item_dict)
            self.add_item(item)

    def save(self, path):
        items = list(self._items.values())
        self._database.saving_data(path, items)

