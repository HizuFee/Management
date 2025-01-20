#views\main_view.py
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from controllers.item_controller import ItemController
from controllers.auth_controller import AuthController
from controllers.category_controller import CategoryController
from models.audit import Audit
from utils.helpers import format_rupiah
import mysql.connector
from tkinter import Text


class InventoryApp(ttk.Window):
    def __init__(self, login_window):
        super().__init__(themename="cosmo")
        self.login_window = login_window
        self.title("Inventory Management")
        self.geometry("1200x600")
        self.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        # Search bar
        search_frame = ttk.Frame(self, padding=(10, 5))
        search_frame.pack(fill=X)

        ttk.Label(search_frame, text="Search:", font=("Arial", 10)).pack(side=LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=LEFT, padx=(0, 10), fill=X, expand=True)
        self.category_filter = ttk.Combobox(search_frame, width=20)
        self.category_filter.pack(side=LEFT, padx=(0, 10))
        self.category_filter.bind('<<ComboboxSelected>>', self.filter_by_category)
        ttk.Button(search_frame, text="Search", command=self.search_item, bootstyle=PRIMARY).pack(side=LEFT, padx=5)

        
        self.update_category_filter()

        ttk.Button(search_frame, text="Refresh", command=self.load_data, bootstyle=INFO).pack(side=LEFT, padx=5)

        ttk.Button(search_frame, text="Logout", command=self.logout, bootstyle=DANGER).pack(side=RIGHT, padx=5)

        # Treeview (Table)
        tree_frame = ttk.Labelframe(self, text="Inventory Items", padding=(10, 5))
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=(5, 10))

        # Create a style for the Treeview
        style = ttk.Style()
        style.configure(
            "Treeview",
            font=("Arial", 10),
            rowheight=5, 
            background="white",
            fieldbackground="white",
            bordercolor="#cccccc",
            borderwidth=1,
        )
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.map("Treeview", background=[("selected", "#cce5ff")])  

        
        style.layout("Treeview", [
            ("Treeview.treearea", {"sticky": "nswe", "border": "1"}) 
        ])

        

        # Add scrollbars
        scrollbar_y = ttk.Scrollbar(tree_frame, orient=VERTICAL)
        scrollbar_y.pack(side=RIGHT, fill=Y)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
        scrollbar_x.pack(side=BOTTOM, fill=X)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Quantity", "Price", "Description", "Category", "Unit"),
            show="headings",
            bootstyle="info",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
        )


        scrollbar_y.config(command=self.tree.yview)
        scrollbar_x.config(command=self.tree.xview)

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Unit", text="Unit")

        self.tree.column("ID", width=50, anchor=CENTER)
        self.tree.column("Name", width=150, anchor=W)
        self.tree.column("Quantity", width=80, anchor=CENTER)
        self.tree.column("Price", width=100, anchor=E)
        self.tree.column("Description", width=250, anchor=CENTER)
        self.tree.column("Category", width=120, anchor=W)
        self.tree.column("Unit", width=80, anchor=W)

        self.tree.pack(fill=BOTH, expand=True)

        # Buttons
        button_frame = ttk.Frame(self, padding=(10, 10))
        button_frame.pack(fill=X)

        ttk.Button(button_frame, text="Add Item", command=self.add_item, bootstyle=SUCCESS, width=15).pack(side=LEFT, padx=5)

        # Add Category Management button
        ttk.Button(button_frame, text="Manage kategori", command=self.manage_categories, bootstyle=PRIMARY, width=15).pack(side=LEFT, padx=5)

        ttk.Button(button_frame, text="Update Item", command=self.update_item, bootstyle=WARNING, width=15).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Item", command=self.delete_item, bootstyle=DANGER, width=15).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="View Details", command=self.view_details, bootstyle=INFO, width=15).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Stock In/Out", command=self.manage_stock, bootstyle=PRIMARY, width=15).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="View History", command=self.view_history, bootstyle=SECONDARY, width=15).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Audit Logs", command=self.view_audit_logs, bootstyle=PRIMARY, width=15).pack(side=LEFT, padx=5)

        self.load_data()



    def load_data(self):
        """Load data from database into the treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)
        

        items = ItemController.get_all_items()
        for item in items:
            self.tree.insert(
                "",
                "end",
                values=(
                    item["id"],
                    item["name"],
                    item["quantity"],
                    format_rupiah(item["price"]),  
                    item["description"],
                    item["category_name"] or "N/A",
                    item["unit"]
                )
            )
        
        # Update category filter
        self.update_category_filter()

    def search_item(self):
        """Search for items by name."""
        query = self.search_entry.get()
        for row in self.tree.get_children():
            self.tree.delete(row)

        items = ItemController.search_items(query)
        for item in items:
            category_name = item.get("category_name", "N/A")  
            self.tree.insert(
                "",
                END,
                values=(
                    item["id"],
                    item["name"],
                    item["quantity"],
                    item["price"],
                    item["description"],
                    category_name,
                    item["unit"]
                ),
            )
    
    def add_item(self):
        def submit():
            try:
                name = name_entry.get()
                quantity = int(quantity_entry.get())
                price = float(price_entry.get())
                description = description_entry.get()
                category_id = category_ids[category_var.get()]
                unit = unit_entry.get() or 'pcs'

                ItemController.add_new_item(name, quantity, price, description, category_id, unit)
                self.load_data()
                add_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            
            except mysql.connector.errors.IntegrityError as e:
                show_error_popup(str(e))
            except ValueError as e:
                show_error_popup(str(e))
        def show_error_popup(message):
            """Display an error popup window."""
            error_window = ttk.Toplevel(self)
            error_window.title("Error")
            error_window.geometry("300x150")
            
            ttk.Label(error_window, text="Error!", foreground="red", font=("Arial", 14, "bold")).pack(pady=10)
            ttk.Label(error_window, text=message, wraplength=250, justify="center").pack(pady=5)
            ttk.Button(error_window, text="Close", command=error_window.destroy).pack(pady=10)

        add_window = ttk.Toplevel(self)
        add_window.title("Add Item")
        add_window.geometry("400x500")

        # Get categories for dropdown
        categories = CategoryController.get_all_categories()
        category_ids = {cat["name"]: cat["id"] for cat in categories}

        # Form fields
        ttk.Label(add_window, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(add_window)
        name_entry.pack()

        ttk.Label(add_window, text="Quantity:").pack(pady=5)
        quantity_entry = ttk.Entry(add_window)
        quantity_entry.pack()

        ttk.Label(add_window, text="Price:").pack(pady=5)
        price_entry = ttk.Entry(add_window)
        price_entry.pack()

        ttk.Label(add_window, text="Description:").pack(pady=5)
        description_entry = ttk.Entry(add_window)
        description_entry.pack()

        ttk.Label(add_window, text="Category:").pack(pady=5)
        category_var = ttk.StringVar(add_window)
        category_dropdown = ttk.Combobox(add_window, textvariable=category_var)
        category_dropdown['values'] = list(category_ids.keys())
        category_dropdown.pack()

        ttk.Label(add_window, text="Unit:").pack(pady=5)
        unit_entry = ttk.Entry(add_window)
        unit_entry.insert(0, 'pcs')
        unit_entry.pack()

        ttk.Button(add_window, text="Submit", command=submit).pack(pady=10)


    def manage_categories(self):
        """Open category management window."""
        category_window = ttk.Toplevel(self)
        category_window.title("Category Management")
        category_window.geometry("600x400")

        # Create Treeview for categories
        tree_frame = ttk.Frame(category_window)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        category_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name"),
            show="headings",
            bootstyle="info",
        )

        category_tree.heading("ID", text="ID")
        category_tree.heading("Name", text="Name")

        category_tree.column("ID", width=50)
        category_tree.column("Name", width=200)

        category_tree.pack(fill=BOTH, expand=True)
    
        def load_categories():
            for item in category_tree.get_children():
                category_tree.delete(item)
            categories = CategoryController.get_all_categories()
            for category in categories:
                category_tree.insert("", END, values=(category["id"], category["name"]))
        
        def add_category():
            add_window = ttk.Toplevel(category_window)
            add_window.title("Add Category")
            add_window.geometry("300x150")

            ttk.Label(add_window, text="Category Name:").pack(pady=5)
            name_entry = ttk.Entry(add_window)
            name_entry.pack(pady=5)

            def submit():
                CategoryController.add_new_category(name_entry.get())
                load_categories()
                add_window.destroy()

            ttk.Button(add_window, text="Submit", command=submit).pack(pady=10)

        def update_category():
            selected = category_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a category to update.")
                return

            category_id = category_tree.item(selected[0], "values")[0]
            category = CategoryController.get_category_by_id(category_id)

            update_window = ttk.Toplevel(category_window)
            update_window.title("Update Category")
            update_window.geometry("300x150")

            ttk.Label(update_window, text="Category Name:").pack(pady=5)
            name_entry = ttk.Entry(update_window)
            name_entry.insert(0, category["name"])
            name_entry.pack(pady=5)

            def submit():
                CategoryController.update_category(category_id, name_entry.get())
                load_categories()
                update_window.destroy()

            ttk.Button(update_window, text="Submit", command=submit).pack(pady=10)

        def delete_category():
            selected = category_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a category to delete.")
                return

            category_id = category_tree.item(selected[0], "values")[0]
            if messagebox.askyesno("Confirm", "Are you sure you want to delete this category?"):
                CategoryController.delete_category(category_id)
                load_categories()

        # Button frame
        button_frame = ttk.Frame(category_window)
        button_frame.pack(fill=X, padx=10, pady=5)

        ttk.Button(button_frame, text="Add Category", command=add_category).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Update Category", command=update_category).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Category", command=delete_category).pack(side=LEFT, padx=5)

        load_categories()

    def update_item(self):
        """Update selected item."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to update.")
            return

        item_id = self.tree.item(selected_item, "values")[0]

        def submit():
            try:
                name = name_entry.get()
                quantity = int(quantity_entry.get())
                price = float(price_entry.get())
                description = description_entry.get()
                category_id = category_ids[category_var.get()]
                unit = unit_entry.get() or 'pcs'

                ItemController.update_item(item_id, name, quantity, price, description, category_id, unit)
                self.load_data()
                update_window.destroy()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        update_window = ttk.Toplevel(self)
        update_window.title("Update Item")
        update_window.geometry("400x500")

        item = ItemController.get_item_by_id(item_id)
        categories = CategoryController.get_all_categories()
        category_ids = {cat["name"]: cat["id"] for cat in categories}

        # Form fields
        ttk.Label(update_window, text="Name:").pack(pady=5)
        name_entry = ttk.Entry(update_window)
        name_entry.insert(0, item["name"])
        name_entry.pack()

        ttk.Label(update_window, text="Quantity:").pack(pady=5)
        quantity_entry = ttk.Entry(update_window)
        quantity_entry.insert(0, item["quantity"])
        quantity_entry.pack()

        ttk.Label(update_window, text="Price:").pack(pady=5)
        price_entry = ttk.Entry(update_window)
        price_entry.insert(0, item["price"])
        price_entry.pack()

        ttk.Label(update_window, text="Description:").pack(pady=5)
        description_entry = ttk.Entry(update_window)
        description_entry.insert(0, item["description"])
        description_entry.pack()

        ttk.Label(update_window, text="Category:").pack(pady=5)
        category_var = ttk.StringVar(update_window)
        category_dropdown = ttk.Combobox(update_window, textvariable=category_var)
        category_dropdown['values'] = list(category_ids.keys())
        
        # Find and select current category
        current_category = next(
            (cat["name"] for cat in categories if cat["id"] == item["category_id"]),
            list(category_ids.keys())[0] if category_ids else ""
        )
        category_var.set(current_category)
        category_dropdown.pack()

        ttk.Label(update_window, text="Unit:").pack(pady=5)
        unit_entry = ttk.Entry(update_window)
        unit_entry.insert(0, item.get("unit", "pcs"))
        unit_entry.pack()

        ttk.Button(update_window, text="Submit", command=submit, bootstyle=SUCCESS).pack(pady=10)

    def delete_item(self):
        """Delete selected item."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to delete.")
            return

        item_id = self.tree.item(selected_item, "values")[0]
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this item?")
        if confirm:
            ItemController.delete_item(item_id)
            self.load_data()

    def view_details(self):
        """View details of the selected item."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to view details.")
            return

        item_id = self.tree.item(selected_item, "values")[0]
        item = ItemController.get_item_by_id(item_id)
        
        # Get category name
        category = CategoryController.get_category_by_id(item["category_id"]) if item["category_id"] else None
        category_name = category["name"] if category else "N/A"

        detail_window = ttk.Toplevel(self)
        detail_window.title("Item Details")
        detail_window.geometry("400x400")

        frame = ttk.Frame(detail_window, padding="20")
        frame.pack(fill=BOTH, expand=True)

        details = [
            ("Name", item["name"]),
            ("Quantity", f"{item['quantity']} {item['unit']}"),
            ("Price", f"Rp {format(item['price'], ',.2f')}"),
            ("Category", category_name),
            ("Unit", item["unit"]),
            ("Description", item["description"]),
        ]

        for label, value in details:
            row = ttk.Frame(frame)
            row.pack(fill=X, pady=5)
            ttk.Label(row, text=f"{label}:", width=15, anchor=W).pack(side=LEFT)
            ttk.Label(row, text=str(value), anchor=W).pack(side=LEFT, fill=X, expand=True)
    

    def manage_stock(self): 
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to manage stock.")
            return

        item_id = self.tree.item(selected_item, "values")[0]
        
        def submit():
            change_type = change_type_var.get()
            quantity_change = int(quantity_entry.get())
            admin_id = AuthController.get_logged_in_admin_id()  
            if admin_id is None:
                messagebox.showerror("Error", "No admin is logged in!")
                return
            ItemController.update_item_stock(item_id, change_type, quantity_change, admin_id)
            self.load_data()
            stock_window.destroy()

        stock_window = ttk.Toplevel(self)
        stock_window.title("Manage Stock")
        stock_window.geometry("300x200")

        ttk.Label(stock_window, text="Change Type:").pack()
        change_type_var = ttk.StringVar(value="in")
        ttk.Radiobutton(stock_window, text="Stock In", variable=change_type_var, value="in").pack()
        ttk.Radiobutton(stock_window, text="Stock Out", variable=change_type_var, value="out").pack()

        ttk.Label(stock_window, text="Quantity:").pack()
        quantity_entry = ttk.Entry(stock_window)
        quantity_entry.pack()

        ttk.Button(stock_window, text="Submit", command=submit, bootstyle=SUCCESS).pack(pady=10)

    
    # Fungsi view_history
    def view_history(self):
        history_window = ttk.Toplevel(self)
        history_window.title("History")
        history_window.geometry("700x400")

        tree = ttk.Treeview(
            history_window,
            columns=("ID", "Item", "Admin", "Type", "Quantity", "Timestamp"),
            show="headings",
            bootstyle="accent-info",
        )
        tree.heading("ID", text="ID", anchor=W)
        tree.heading("Item", text="Item", anchor=W)
        tree.heading("Admin", text="Admin", anchor=W)
        tree.heading("Type", text="Type", anchor=W)
        tree.heading("Quantity", text="Quantity", anchor=W)
        tree.heading("Timestamp", text="Timestamp", anchor=W)

        tree.column("ID", width=50, anchor=W)
        tree.column("Item", width=150, anchor=W)
        tree.column("Admin", width=100, anchor=W)
        tree.column("Type", width=50, anchor=W)
        tree.column("Quantity", width=50, anchor=W)
        tree.column("Timestamp", width=150, anchor=W)

        tree.pack(fill=BOTH, expand=True)

        history = ItemController.get_all_history()
        for record in history:
            tree.insert(
                "",
                END,
                values=(
                    record["id"],
                    record["item_name"],
                    record["admin_name"],
                    record["change_type"],
                    record["quantity_change"],
                    record["timestamp"],
                ),
            )
    def update_category_filter(self):
        """Update the category filter dropdown with current categories"""
        categories = CategoryController.get_all_categories()
        category_list = ["All"] + [cat["name"] for cat in categories]
        self.category_filter['values'] = category_list
        self.category_filter.set("All")

    def filter_by_category(self, event=None):
        """Filter items by selected category"""
        selected_category = self.category_filter.get()
        
        
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if selected_category == "All":
            items = ItemController.get_all_items()
        else:
            # Get category ID
            categories = CategoryController.get_all_categories()
            category_id = next((cat["id"] for cat in categories if cat["name"] == selected_category), None)
            items = ItemController.get_all_items(category_id)
        
        
        for item in items:
            self.tree.insert(
                "",
                "end",
                values=(
                    item["id"],
                    item["name"],
                    item["quantity"],
                    item["price"],
                    item["description"],
                    item["category_name"] or "N/A",
                    item["unit"]
                )
            )
    def view_audit_logs(self):
        audit_window = ttk.Toplevel(self)
        audit_window.title("Audit Logs")
        audit_window.geometry("1000x600")

        filter_frame = ttk.Frame(audit_window, padding=10)
        filter_frame.pack(fill=X)

        ttk.Label(filter_frame, text="Table:").pack(side=LEFT, padx=5)
        table_filter = ttk.Combobox(filter_frame, values=['items', 'categories'], state="readonly")
        table_filter.pack(side=LEFT, padx=5)

        ttk.Label(filter_frame, text="Action:").pack(side=LEFT, padx=5)
        action_filter = ttk.Combobox(filter_frame, values=['INSERT', 'UPDATE', 'DELETE'], state="readonly")
        action_filter.pack(side=LEFT, padx=5)

        tree_frame = ttk.Frame(audit_window)
        tree_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Table", "Record ID", "Action", "Admin", "Timestamp"),
            show="headings",
            bootstyle="info",
        )

        tree.heading("ID", text="ID")
        tree.heading("Table", text="Table")
        tree.heading("Record ID", text="Record ID")
        tree.heading("Action", text="Action")
        tree.heading("Admin", text="Admin")
        tree.heading("Timestamp", text="Timestamp")

        tree.column("ID", width=50, anchor=CENTER)
        tree.column("Table", width=100, anchor=CENTER)
        tree.column("Record ID", width=80, anchor=CENTER)
        tree.column("Action", width=80, anchor=CENTER)
        tree.column("Admin", width=100, anchor=CENTER)
        tree.column("Timestamp", width=150, anchor=CENTER)

        scrollbar = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        tree.pack(fill=BOTH, expand=True)

        details_frame = ttk.LabelFrame(audit_window, text="Change Details", padding=10)
        details_frame.pack(fill=BOTH, padx=10, pady=5, expand=True)

        details_text = Text(details_frame, height=12, wrap=WORD)
        details_text.pack(fill=BOTH, expand=True)

        def load_audit_logs():
            """Load and display audit logs in the Treeview."""
            for item in tree.get_children():
                tree.delete(item)

            filters = {}
            if table_filter.get():
                filters['table_name'] = table_filter.get()
            if action_filter.get():
                filters['action_type'] = action_filter.get()

            logs = Audit.get_audit_logs(filters)

            for log in logs:
                tree.insert("", "end", values=(
                    log['id'],
                    log['table_name'],
                    log['record_id'],
                    log['action_type'],
                    log['admin_name'],
                    log['timestamp']
                ))

        def show_details(event):
            """Display detailed changes for the selected audit log."""
            selected = tree.selection()
            if not selected:
                details_text.delete("1.0", "end")
                details_text.insert("1.0", "No log selected.")
                return

            log_id = tree.item(selected[0])['values'][0]
            
            log = Audit.get_audit_log_by_id(log_id)
            
            if not log:
                details_text.delete("1.0", "end")
                details_text.insert("1.0", f"No details found for log ID: {log_id}")
                return

            details_text.delete("1.0", "end")

            details = f"Log ID: {log['id']}\n"
            details += f"Table: {log['table_name']}\n"
            details += f"Record ID: {log['record_id']}\n"
            details += f"Action: {log['action_type']}\n"
            details += f"Admin: {log['admin_name']}\n"
            details += f"Timestamp: {log['timestamp']}\n\n"

            if log['old_values']:
                details += "Old Values:\n"
                for key, value in log['old_values'].items():
                    details += f"  {key}: {value}\n"

            if log['new_values']:
                details += "\nNew Values:\n"
                for key, value in log['new_values'].items():
                    details += f"  {key}: {value}\n"

            details_text.insert("1.0", details)

        tree.bind("<<TreeviewSelect>>", show_details)
        table_filter.bind("<<ComboboxSelected>>", lambda e: load_audit_logs())
        action_filter.bind("<<ComboboxSelected>>", lambda e: load_audit_logs())

        ttk.Button(filter_frame, text="Refresh", command=load_audit_logs).pack(side=RIGHT, padx=5)

        load_audit_logs()

    
    

    def logout(self):
        AuthController.logged_in_admin_id = None 
        messagebox.showinfo("Info", "Successfully logged out.")
        self.login_window.deiconify()  
        self.destroy()  



if __name__ == "__main__":
    app = InventoryApp()
    app.mainloop()
