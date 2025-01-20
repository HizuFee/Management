# models/item.py
from config.database import get_connection
from models.audit import Audit
from controllers.auth_controller import AuthController
class Item:
    @staticmethod
    def get_all(sort_by_category=None):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if sort_by_category:
            cursor.execute("""
                SELECT i.*, c.name as category_name 
                FROM items i 
                LEFT JOIN categories c ON i.category_id = c.id 
                WHERE i.category_id = %s AND i.is_deleted = 0
            """, (sort_by_category,))
        else:
            cursor.execute("""
                SELECT i.*, c.name as category_name 
                FROM items i 
                LEFT JOIN categories c ON i.category_id = c.id 
                WHERE i.is_deleted = 0
            """)
        result = cursor.fetchall()
        conn.close()
        return result
    @staticmethod
    def add_item(name, quantity, price, description, category_id, unit='pcs'):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """INSERT INTO items (name, quantity, price, description, category_id, unit) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (name, quantity, price, description, category_id, unit),
        )
        
        item_id = cursor.lastrowid
        
        new_values = {
            'name': name,
            'quantity': quantity,
            'price': price,
            'description': description,
            'category_id': category_id,
            'unit': unit
        }
        
        admin_id = AuthController.get_logged_in_admin_id()
        Audit.log_change('items', item_id, 'INSERT', None, new_values, admin_id)
        
        conn.commit()
        conn.close()

    @staticmethod
    def update_item(item_id, name, quantity, price, description, category_id, unit='pcs'):
        # Get old values first
        old_item = Item.get_item_by_id(item_id)
        old_values = {
            'name': old_item['name'],
            'quantity': old_item['quantity'],
            'price': old_item['price'],
            'description': old_item['description'],
            'category_id': old_item['category_id'],
            'unit': old_item['unit']
        }
        
        # Update the item
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE items 
            SET name=%s, quantity=%s, price=%s, description=%s, category_id=%s, unit=%s 
            WHERE id=%s""",
            (name, quantity, price, description, category_id, unit, item_id),
        )
        
        # Log the audit
        new_values = {
            'name': name,
            'quantity': quantity,
            'price': price,
            'description': description,
            'category_id': category_id,
            'unit': unit
        }
        
        admin_id = AuthController.get_logged_in_admin_id()
        Audit.log_change('items', item_id, 'UPDATE', old_values, new_values, admin_id)
        
        conn.commit()
        conn.close()

    @staticmethod
    def delete_item(item_id):
        # Get old values first
        old_item = Item.get_item_by_id(item_id)
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id=%s", (item_id,))
        
        # Log the audit
        admin_id = AuthController.get_logged_in_admin_id()
        Audit.log_change('items', item_id, 'DELETE', old_item, None, admin_id)
        
        conn.commit()
        conn.close()

    @staticmethod
    def get_item_by_id(item_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.*, c.name as category_name 
            FROM items i 
            LEFT JOIN categories c ON i.category_id = c.id 
            WHERE i.id = %s AND i.is_deleted = 0
        """, (item_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def search_items(query):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM items WHERE name LIKE %s", (f"%{query}%",)
        )
        result = cursor.fetchall()
        conn.close()
        return result
    
    @staticmethod
    def get_items_by_category(category_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.*, c.name as category_name 
            FROM items i 
            LEFT JOIN categories c ON i.category_id = c.id 
            WHERE i.category_id = %s AND i.is_deleted = 0
        """, (category_id,))
        result = cursor.fetchall()
        conn.close()
        return result
    
class History:
    @staticmethod
    def log_change(item_id, admin_id, change_type, quantity_change):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO history (item_id, admin_id, change_type, quantity_change) VALUES (%s, %s, %s, %s)",
            (item_id, admin_id, change_type, quantity_change),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_history():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT h.id, i.name AS item_name, a.username AS admin_name, h.change_type, h.quantity_change, h.timestamp "
            "FROM history h "
            "JOIN items i ON h.item_id = i.id "
            "JOIN admin a ON h.admin_id = a.id "
            "ORDER BY h.timestamp DESC"
        )
        result = cursor.fetchall()
        conn.close()
        return result
    
   
