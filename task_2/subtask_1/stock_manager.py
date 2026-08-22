PATH = "stock.txt"

def open_file(path:str) -> dict:
    """
    Function to open the file safely
    it takes only the file path as parameter and returns a dict of 
    the contet of the file as "key"(name of the fruit): "value"(quantity)  
    """
    try:
        stock = {}
        with open(path) as file:
            rows = file.readlines()
            for row in rows:
                key_value = list(row.strip().split(","))
                stock[key_value[0].strip().lower()] = int(key_value[1].strip())

    except FileNotFoundError:
        raise Exception("Error while opening the file")
    except Exception as e:
        raise Exception(f"Error occured {e}")

    return stock


def menu_display() -> int:
    """
    Function to safely take the required operation 
    from the user and return it 
    """
    values = ('1', "2", "3", "4")

    while True:
        x = input("""\nenter 1 to add stock
enter 2 to remove stock
enter 3 to show stock’s contents
enter 4 to exit the program
>>> """).strip()
        
        if x in values:
            return int(x)
        else:
            print("\n--Please Enter a valid number---")


def stock_display(stock:dict) -> None:
    """
    Function to display stock in readable format
    """
    print("-" * 15)
    for id, (key, value) in enumerate(stock.items()):
        print(f"{id+1}. {key}: {value}")


def key_input(stock:dict) -> str:
    while True:
        x = input("""Enter stock name or id
e.g. enter “banana” or “1” to change banana stock or enter “Dates” for a new stock\n>>> """).strip()

        if x.isdigit() and 1 <= int(x) <= len(stock):
            x = int(x)
            return list((stock.keys()))[x-1]
        elif x.isalpha():
            return x.lower()
        else:
            print("---Enter a valid input---")

def value_input() -> int:
    while True:
        x = input("Enter the amount: ").strip()
        if x.isdigit():
            return int(x)
        else:
            print("Please Enter a valid amount")
            


def adding(stock:dict):
    stock_display(stock)
    key = key_input(stock)
    value = value_input()

    if key in stock:
        stock[key] += value
    else:
        stock[key] = value
    stock_display(stock)


def removing(stock:dict):
    while True:
        stock_display(stock)
        key = key_input(stock)
        value = value_input()

        if key not in stock:
            print("---Please Enter a name from the stock---")
        else:
            if stock[key] - value < 0:
                print("--Value is too large can't be removed enter a valid amount---")
            else:
                stock[key] -= value
                break

    stock_display(stock)

def save_prog(stock:dict, path):
    with open(path, 'w') as file:
        for key, value in stock.items():
            file.write(f"{key},{value}\n")

if __name__ == "__main__":

    stock = open_file(PATH)
   
    while True:
        inp = menu_display()

        if inp == 1:
            adding(stock)
        elif inp == 2:
            removing(stock)
        elif inp == 3:
            stock_display(stock)
        elif inp == 4:
            save_prog(stock, PATH)
            break

