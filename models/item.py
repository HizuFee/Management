from config.database import get_connection

class Item:
    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def add_item(name, quantity, price):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO items (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
        conn.commit()
        conn.close()
