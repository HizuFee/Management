from models.item import Item

class ItemController:
    @staticmethod
    def get_all_items():
        return Item.get_all()

    @staticmethod
    def add_new_item(name, quantity, price):
        Item.add_item(name, quantity, price)
