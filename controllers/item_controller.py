# controllers/item_controller.py
from models.item import Item
from models.item import History


class ItemController:
    
    @staticmethod
    def get_all_items(sort_by_category=None):
        if sort_by_category and sort_by_category != "All":
            return Item.get_items_by_category(sort_by_category)
        return Item.get_all()

    @staticmethod
    def add_new_item(name, quantity, price, description, category, unit='pcs'):
        Item.add_item(name, quantity, price, description, category, unit)

    @staticmethod
    def update_item(item_id, name, quantity, price, description, category, unit='pcs'):
        Item.update_item(item_id, name, quantity, price, description, category, unit)

    @staticmethod
    def get_unique_categories():
        return Item.get_categories()

    @staticmethod
    def delete_item(item_id):
        Item.delete_item(item_id)

    @staticmethod
    def get_item_by_id(item_id):
        return Item.get_item_by_id(item_id)

    @staticmethod
    def search_items(query):
        return Item.search_items(query)
    @staticmethod
    def get_items_by_category(category_name):
        if category_name == "All":
            return Item.get_all()
        return Item.get_items_by_category(category_name)
    

    @staticmethod
    def update_item_stock(item_id, change_type, quantity_change, admin_id):
        item = Item.get_item_by_id(item_id)
        new_quantity = item["quantity"] + quantity_change if change_type == "in" else item["quantity"] - quantity_change
        if new_quantity < 0:
            raise ValueError("Insufficient stock for this operation.")
        Item.update_item(item_id, item["name"], new_quantity, item["price"], item["description"], item["category_id"])
        History.log_change(item_id, admin_id, change_type, quantity_change)
    @staticmethod
    def log_stock_change(item_id, admin_id, change_type, quantity_change):
        History.log_change(item_id, admin_id, change_type, quantity_change)

    @staticmethod
    def get_all_history():
        return History.get_history()
    
    