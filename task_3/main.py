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

d_dvd = {"type": "DVD", "title": "Inception", "director": "Christopher Nolan", "status": "CHECKED_OUT"}
d_magazine = {"type": "Magazine", "title": "National Geographic", "issue": "2026-08", "status": "AVAILABLE"}
d_book = {"type": "Book", "title": "1984", "author": "George Orwell", "isbn": "9780451524935", "status": "CHECKED_OUT"}

book = LibraryItem.from_dict(d_book)
print(book)
print(repr(book))
print(book.author, book.isbn)

mag = LibraryItem.from_dict(d_magazine)
print(mag)
print(repr(mag))
print(mag.issue)

dvd = LibraryItem.from_dict(d_dvd)
print(dvd)
print(repr(dvd))
print(dvd.director)