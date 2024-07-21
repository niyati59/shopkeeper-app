import json
import os
import time
from tqdm import tqdm
from tabulate import tabulate

class Item:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def to_dict(self):
        return {'name': self.name, 'price': self.price, 'quantity': self.quantity}

    @staticmethod
    def from_dict(data):
        return Item(data['name'], data['price'], data['quantity'])

    def __repr__(self):
        return f"Item(name={self.name}, price={self.price}, quantity={self.quantity})"


class Shopkeeper:
    def __init__(self, inventory_file='inventory.json', sales_file='sales.json'):
        self.inventory = {}
        self.sales = []
        self.inventory_file = inventory_file
        self.sales_file = sales_file
        self.load_inventory()
        self.load_sales()

    def add_item(self, name, price, quantity):
        if name in self.inventory:
            self.inventory[name].quantity += quantity
        else:
            self.inventory[name] = Item(name, price, quantity)
        self.save_inventory()

    def remove_item(self, name):
        if name in self.inventory:
            del self.inventory[name]
            self.save_inventory()
            print(f"Item {name} removed from inventory.")
        else:
            print(f"Item {name} not found in inventory.")

    def update_item(self, name, price=None, quantity=None):
        if name in self.inventory:
            if price is not None:
                self.inventory[name].price = price
            if quantity is not None:
                self.inventory[name].quantity = quantity
            self.save_inventory()
            print(f"Item {name} updated.")
        else:
            print(f"Item {name} not found in inventory.")

    def sell_item(self, name, quantity):
        if name in self.inventory and self.inventory[name].quantity >= quantity:
            self.inventory[name].quantity -= quantity
            total_price = self.inventory[name].price * quantity
            self.sales.append({'name': name, 'quantity': quantity, 'total_price': total_price})
            self.save_inventory()
            self.save_sales()
            return total_price
        else:
            print("Item not available or insufficient quantity")
            return 0

    def show_inventory(self, sort_by=None):
        items = list(self.inventory.values())
        if sort_by == 'name':
            items.sort(key=lambda x: x.name)
        elif sort_by == 'price':
            items.sort(key=lambda x: x.price)
        elif sort_by == 'quantity':
            items.sort(key=lambda x: x.quantity)
        
        table = [[item.name, item.price, item.quantity] for item in items]
        print(tabulate(table, headers=["Name", "Price", "Quantity"], tablefmt="grid"))

    def show_sales(self):
        table = [[sale['name'], sale['quantity'], sale['total_price']] for sale in self.sales]
        print(tabulate(table, headers=["Name", "Quantity", "Total Price"], tablefmt="grid"))

    def search_item(self, name):
        if name in self.inventory:
            item = self.inventory[name]
            table = [[item.name, item.price, item.quantity]]
            print(tabulate(table, headers=["Name", "Price", "Quantity"], tablefmt="grid"))
        else:
            print(f"Item {name} not found in inventory.")

    def generate_report(self):
        total_sales = sum(sale['total_price'] for sale in self.sales)
        print(f"Total Sales: ${total_sales}\n")
        print("Inventory Report:")
        self.show_inventory()

    def save_inventory(self):
        with open(self.inventory_file, 'w') as f:
            json.dump({name: item.to_dict() for name, item in self.inventory.items()}, f)

    def load_inventory(self):
        if not os.path.exists(self.inventory_file):
            with open(self.inventory_file, 'w') as f:
                json.dump({}, f)
        else:
            try:
                with open(self.inventory_file, 'r') as f:
                    data = json.load(f)
                    self.inventory = {name: Item.from_dict(item) for name, item in data.items()}
            except json.JSONDecodeError:
                self.inventory = {}

    def save_sales(self):
        with open(self.sales_file, 'w') as f:
            json.dump(self.sales, f)

    def load_sales(self):
        if not os.path.exists(self.sales_file):
            with open(self.sales_file, 'w') as f:
                json.dump([], f)
        else:
            try:
                with open(self.sales_file, 'r') as f:
                    self.sales = json.load(f)
            except json.JSONDecodeError:
                self.sales = []


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_bar():
    for _ in tqdm(range(100), desc="Loading", ncols=75):
        time.sleep(0.03)
    clear_screen()


def main():
    shopkeeper = Shopkeeper()
    
    while True:
        print("\n1. Add Item")
        print("2. Remove Item")
        print("3. Update Item")
        print("4. Sell Item")
        print("5. Show Inventory")
        print("6. Search Item")
        print("7. Show Sales")
        print("8. Generate Report")
        print("9. Exit")
        choice = input("Enter your choice: ")

        clear_screen()

        if choice == '1':
            loading_bar()
            name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            quantity = int(input("Enter item quantity: "))
            shopkeeper.add_item(name, price, quantity)
        elif choice == '2':
            loading_bar()
            name = input("Enter item name to remove: ")
            shopkeeper.remove_item(name)
        elif choice == '3':
            loading_bar()
            name = input("Enter item name to update: ")
            price = input("Enter new price (or press Enter to skip): ")
            quantity = input("Enter new quantity (or press Enter to skip): ")
            price = float(price) if price else None
            quantity = int(quantity) if quantity else None
            shopkeeper.update_item(name, price, quantity)
        elif choice == '4':
            loading_bar()
            print("Available Products:")
            shopkeeper.show_inventory()
            name = input("Enter item name: ")
            quantity = int(input("Enter quantity to sell: "))
            total_price = shopkeeper.sell_item(name, quantity)
            if total_price:
                print(f"Sold {quantity} of {name} for ${total_price}")
        elif choice == '5':
            loading_bar()
            sort_by = input("Sort inventory by (name, price, quantity) or press Enter to skip: ")
            shopkeeper.show_inventory(sort_by if sort_by in ['name', 'price', 'quantity'] else None)
        elif choice == '6':
            loading_bar()
            name = input("Enter item name to search: ")
            shopkeeper.search_item(name)
        elif choice == '7':
            loading_bar()
            shopkeeper.show_sales()
        elif choice == '8':
            loading_bar()
            shopkeeper.generate_report()
        elif choice == '9':
            loading_bar()
            break
        else:
            print("Invalid choice, please try again.")

        input("Press Enter to continue...")
        clear_screen()
        loading_bar()


if __name__ == "__main__":
    main()
