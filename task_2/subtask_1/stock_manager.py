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
                stock[key_value[0]] = int(key_value[1])

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
        x = input("""enter 1 to add stock
enter 2 to remove stock
enter 3 to show stock’s contents
enter 4 to exit the program
>>> """).strip()
        
        if x in values:
            return int(x)
        else:
            print("\n--Please Enter a valid number---")


if __name__ == "__main__":
    menu_display()
    

