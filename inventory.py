from tabulate import tabulate


class Shoes:  # Shoe class

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        # A comma separated string representation of a class
        return f"{self.country}, {self.code}, {self.product}, {self.cost}, {self.quantity}"


shoes_list = []  # An empty list to store shoe objects
shoe_list_head = []  # An empty list to store headings


# The following is_yes_no function is adapted from Capstone Project III by Fortune Ncube
def is_yes_no(yes_no):
    """
    This function checks if a string input is either a 'yes' or 'no'.
    The continues to run until one of the options above is true.
    :param yes_no:
    :return: yes_no
    """
    while True:
        if yes_no not in ["yes", "no"]:
            yes_no = input(f"\nIncorrect input: {yes_no} \nPlease enter either 'Yes' or 'No'")
        else:
            break
    return yes_no  # If yes_no is either 'yes' or 'no' then return yes_no as is


def read_shoes_data():
    with open("inventory.txt", "r", encoding="utf-8-sig") as inventory_data:
        for prod_count, prod_info in enumerate(inventory_data.read().splitlines()):
            prod = prod_info.split(sep=',')  # Split each line into a list
            if not prod_count == 0:  # Only capture data for all rows but one
                try:
                    if len(prod) < 5:  # Each row can only be split into 5 list elements
                        raise ValueError("Incomplete_Data")
                    elif len(prod) > 5:
                        raise ValueError("Excess_Data")
                    # The last 2 elements must allow to be cast to float and int types
                    elif prod[3].isnumeric() and prod[4].isnumeric():
                        shoe = Shoes(prod[0], prod[1], prod[2], prod[3], prod[4])
                        shoes_list.append(shoe)
                    else:
                        raise ValueError("Non_Numerical_Value")
                except ValueError as err:
                    print("\n", err, ":", prod_info, "\n")
            else:  # Data from first row represents table headings
                heads = str(Shoes(prod[0], prod[1], prod[2], prod[3], prod[4])).split(",")
                shoe_list_head.append(heads)


def capture_shoes():
    shoe_country = input("Please enter the country where shoe is manufactured\n:")
    code_shoe = input("Please enter the SKU code of the shoe\n:").upper()
    shoe_product = input("Please enter the product name of the shoe\n:")

    while True:
        try:
            shoe_cost = input("Please enter the cost of each pair for this shoe\n:")
            shoe_quantity = input("How many shoes of this type does the store have?\n:")

            # Shoe cost and quantity must be cast able to float and int respectively
            if not float(shoe_cost):
                raise ValueError("Error: Cost of shoe must be in digital format.\n")
            elif not shoe_quantity.isdigit():
                raise ValueError("Error: Quantity of shoe must be in digital format and an Integer.\n")
        except ValueError as err:
            print(err)
        else:
            break

    # Create shoe instance and append it to a list of shoes
    shoe = Shoes(shoe_country, code_shoe, shoe_product, shoe_cost, shoe_quantity)
    shoes_list.append(shoe)

    # Option to permanently add shoe in inventory
    add_inv = input("Would you like to add the shoe in Inventory? Yes or No\n")
    if is_yes_no(add_inv) == "yes":

        # Append the captured shoe to a list of shoes
        with open("inventory.txt", "a", encoding="utf-8-sig") as inventory_data:

            shoe_info = [shoe.country,
                         shoe.code,
                         shoe.product,
                         str(shoe.cost),
                         str(shoe.quantity),
                         ]

            inventory_data.write(",".join(shoe_info) + "\n")
        print("\nShoe has been added in Inventory")
    else:
        print("\nShoe has not been added in Inventory")


def view_all():

    shoe_objs = []  # An empty list to store all string representations of shoe objects
    for shoe_pair in shoes_list:
        shoe_objs.append(str(shoe_pair).split(","))  # EAch object is stored as a list of its attributes

    head = shoe_list_head[0]  # Retrieve headings
    print(tabulate(shoe_objs, headers=head, tablefmt="grid"))  # Tabulate all shoe object attributes


def add_to_inv():
    with open("inventory.txt", "w+", encoding="utf-8-sig") as inventory_data:
        inventory_data.write(",".join(shoe_list_head[0]) + "\n")  # Writing the headings to file first before shoes
        for shoe_data in shoes_list:
            shoe_info = [shoe_data.country,
                         shoe_data.code,
                         shoe_data.product,
                         str(shoe_data.cost),
                         str(shoe_data.quantity),
                         ]
            inventory_data.write(",".join(shoe_info) + "\n")


def re_stock():
    min_stock = list(int(shoe.quantity) for shoe_ind, shoe in enumerate(shoes_list))

    mini = min(min_stock)
    mini_quantities = []  # Stores list, each list has the minimum value and its index in shoes_lists

    # It is possible to have multiple minimum stock values
    for shoe_ind, quant in enumerate(min_stock):
        if quant == mini:
            mini_quantities.append([quant, shoe_ind])

    stock_added = False
    for re_stock_item in mini_quantities:
        shoe_index = re_stock_item[1]
        shoe_stock = shoes_list[shoe_index]

        print(f"\nThe following shoe has a stock of {shoe_stock.quantity} items left.")
        print(f"Country: {shoe_stock.country} \nCode: {shoe_stock.code} \nProduct Name: {shoe_stock.product}")

        add_stock = input(f"\nWould you like to re stock {shoe_stock.product}? Yes or No\n")

        if is_yes_no(add_stock) == "yes":
            while True:
                try:
                    new_quant = input("Please enter quantity to be stocked\n:")
                    if not new_quant.isdigit():
                        raise ValueError("Stocked quantity must be a digital integer.\n")
                except ValueError as err:
                    print(f"%s" % err)

                    try_quant = input("Would you like to try again? Enter Yes or No\n")
                    if is_yes_no(try_quant) == "no":
                        break
                else:
                    shoe_stock.quantity = new_quant
                    stock_added = True
                    break
        else:
            continue

    if stock_added:  # Confirm if a new stocked quantity must be added in inventory
        # Re-writing all captured shoes in a list to a text file
        add_to_inv()


def search_shoe(code_of_shoe):
    for shoe in shoes_list:
        if shoe.code == code_of_shoe:
            print(f"\nThe searched shoe details are:")

            head = shoe_list_head[0]
            print(tabulate([str(shoe).split(",")], headers=head, tablefmt="grid"))


def value_per_item():
    shoe_value = []
    for shoe in shoes_list:
        value = float(shoe.cost) * int(shoe.quantity)

        str_obj = str(shoe).split(",")
        str_obj.append(f"{value}")

        shoe_value.append(str_obj)

    heads = shoe_list_head[0]
    heads.append("Value")

    print(tabulate(shoe_value, headers=heads, tablefmt="grid"))


def highest_quantity():
    stock_quant = list(int(shoe.quantity) for shoe_ind, shoe in enumerate(shoes_list))

    max_quant = max(stock_quant)
    for shoe_ind, quant in enumerate(stock_quant):  # There could be multiple shoes with the same max quantity

        if quant == max_quant:  #

            print("\nThe following shoe is for SALE!!! Hurry while stock last!")
            print(shoes_list[shoe_ind])


def change_cost(shoe_num):
    cost_changed = False
    for shoe in shoes_list:
        if shoe.code == shoe_num:

            while True:
                try:
                    shoe_cost = input(f"Please enter the new cost for this shoe,\n{shoe}\n:")

                    # Shoe cost must be cast able to float
                    if not float(shoe_cost):
                        raise ValueError("Error: Cost of shoe must be in digital format.\n")
                except ValueError as err:
                    print(err)

                    try_shoe_cost = input("Would you like to try again? Enter Yes or No\n")
                    if is_yes_no(try_shoe_cost) == "no":
                        break
                else:
                    shoe.cost = shoe_cost
                    print("Cost of shoe has been updated.")
                    cost_changed = True
                    break
            break

    if cost_changed:  # If there was a successful change in cost, edit the inventory list
        add_to_inv()


read_shoes_data()  # The first thing to do is to read the existing shoe instances
while True:
    inv = input("""\nPlease choose from the options below:
            c - Capture Shoes into Inventory
            v - View All Shoes
            r - Re-stock a Shoe
            m - Change Cost of a Shoe
            s - Search a Shoe
            d - Display Stock Value of each Shoe
            h - Display a Shoe for Sale
            e - Exit \n""").lower()

    if inv == "c":
        capture_shoes()
    elif inv == "v":
        view_all()
    elif inv == "r":
        re_stock()
    elif inv == "m":
        while True:
            view_all()
            shoe_code = input("Please enter a shoe code to change cost of any of the above:\n").upper()
            if shoe_code in list(s_code.code for s_code in shoes_list):
                change_cost(shoe_code)
                break
            else:
                print(f"The Shoe Code: {shoe_code} is not recorded in Inventory.")
                try_cost = input("Would you like to try again? Yes or No\n")
                if is_yes_no(try_cost) == "no":
                    break

    elif inv == "s":
        while True:
            shoe_search = input("Please enter the shoe Code to be searched:\n").upper()

            if shoe_search in list(s_code.code for s_code in shoes_list):
                search_shoe(shoe_search)
                break
            else:
                print(f"The Shoe Code: {shoe_search} is not recorded in Inventory.")
                try_search = input("Would you like to try again? Yes or No\n")
                if is_yes_no(try_search) == "no":
                    break
    elif inv == "d":
        print("\nThe stock Value is Tabulated below:\n")
        value_per_item()
    elif inv == "h":
        highest_quantity()
    elif inv == "e":
        print("Closing Shoe Inventory ...\nGoodbye!!!")
        exit()
    else:
        try_again = input(f"The entered option {inv} is incorrect.\nWould you like to try again? Yes or No\n")
        if is_yes_no(try_again) == "yes":
            continue
        else:
            print("Closing Shoe Inventory ...\nGoodbye!!!")
            exit()
