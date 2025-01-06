import tkinter as tk
from tkinter import ttk, messagebox
from controllers.item_controller import ItemController

class InventoryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Management")
        self.geometry("600x400")
        self.setup_ui()

    def setup_ui(self):
        self.tree = ttk.Treeview(self, columns=("Name", "Quantity", "Price"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.load_data()

        add_button = ttk.Button(self, text="Add Item", command=self.add_item)
        add_button.pack(side=tk.BOTTOM, pady=10)

    def load_data(self):
        items = ItemController.get_all_items()
        for item in items:
            self.tree.insert("", tk.END, values=(item["name"], item["quantity"], item["price"]))

    def add_item(self):
        def submit():
            name = name_entry.get()
            quantity = int(quantity_entry.get())
            price = float(price_entry.get())

            ItemController.add_new_item(name, quantity, price)
            self.load_data()
            add_window.destroy()

        add_window = tk.Toplevel(self)
        add_window.title("Add Item")
        add_window.geometry("300x200")

        tk.Label(add_window, text="Name:").pack()
        name_entry = tk.Entry(add_window)
        name_entry.pack()

        tk.Label(add_window, text="Quantity:").pack()
        quantity_entry = tk.Entry(add_window)
        quantity_entry.pack()

        tk.Label(add_window, text="Price:").pack()
        price_entry = tk.Entry(add_window)
        price_entry.pack()

        ttk.Button(add_window, text="Submit", command=submit).pack(pady=10)
