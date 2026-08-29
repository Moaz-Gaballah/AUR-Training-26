from enum import Enum,auto
from abc import ABC, abstractmethod

class ItemStatus(Enum):
    AVAILABLE = auto()
    CHECKED_OUT = auto()
    LOST = auto()

class LibraryItem(ABC):

    def __init__(self, title):
        self.title = title
        self.__status = ItemStatus.AVAILABLE

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
    def __init__(self, title):
        super().__init__(title)

    def item_type(self):
        return "Book"
       

class DVD(LibraryItem):
    loan_period = 5
    def __init__(self, title):
        super().__init__(title)

    def item_type(self):
        return "DVD"
    
class Magazine(LibraryItem):
    loan_period = 14
    def __init__(self, title):
        super().__init__(title)

    def item_type(self):
        return "Magazine"

print(LibraryItem.isbn_check("9780441013593"))   
print(LibraryItem.isbn_check("9780441013590"))   
print(LibraryItem.isbn_check("hello")) 
print(LibraryItem.isbn_check("123"))        